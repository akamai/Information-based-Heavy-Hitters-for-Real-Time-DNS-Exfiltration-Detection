# Copyright 2023 Akamai Technologies, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

import pandas as pd
import tldextract
import pickle
from config import (
    tuning_dataset_path,
    acceptable_fpr,
    detection_threshold_path,
    global_allowlist_path,
    dns_exf_domains,
    time_window,
    k,
)
from ibHH.InformationBasedHeavyHitter import InformationBasedHeavyHitter
from time import time

from read_dns_queries import read_dns_queries

if __name__ == "__main__":
    filename = tuning_dataset_path
    record_stream = read_dns_queries(filename)
    df_global_allow_list = pd.read_csv(global_allowlist_path, header=None)
    df_global_allow_list = df_global_allow_list.rename(columns={0: "rank", 1: "domain"})
    global_allow_list = set(df_global_allow_list["domain"].tolist())
    current_window = 0
    total_time = 0
    total_time_without_tldextract = 0
    ibhh = None
    count_train = {}
    extract = tldextract.TLDExtract(include_psl_private_domains=False)
    print(f"tuning for acceptable FPR of {acceptable_fpr}")
    for record in record_stream:
        comma_split = record.split(",")
        timestamp = int(comma_split[0])
        dns_query = comma_split[1]
        start_time = time()
        extracted = extract(dns_query)
        domain = extracted.registered_domain.lower()
        subdomain = extracted.subdomain
        start_time_without = time()
        if timestamp > current_window + time_window:
            ibhh = InformationBasedHeavyHitter(k=k)
            current_window = timestamp
        ibhh.add_pair(subdomain, domain)
        count = ibhh.count_domain_information(domain)

        if domain not in count_train or count_train[domain] < count:
            count_train[domain] = count

        end_time = time()
        total_time += end_time - start_time
        total_time_without_tldextract += end_time - start_time_without
    print(
        f"it took {total_time} to process {n} queries, or {n / (total_time)} queries per second"
    )
    print("======= WITHOUT tldextract =======")
    print(
        f"it took {total_time_without_tldextract} to process {n} queries, or {n / (total_time_without_tldextract)} queries per second"
    )

    with open("count_train.pkl", "wb") as f:
        pickle.dump(count_train, f)

    keys = list(
        set(count_train.keys()).difference(global_allow_list.union(dns_exf_domains))
    )
    count_train = {key: count_train[key] for key in keys}
    total = len(count_train)
    acceptable_fps = int(math.ceil(total * acceptable_fpr))
    values = sorted(count_train.values(), reverse=True)
    detection_threshold = values[acceptable_fps] + 1
    with open(detection_threshold_path, "w") as f:
        print(
            f"detection_threshold: {detection_threshold}, or {detection_threshold / 120} B/s"
        )
        f.write(str(detection_threshold))
