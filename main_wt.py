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

import pandas as pd
import tldextract
from config import (
    pt_path,
    global_allowlist_path,
    dns_exf_domains,
    detections_path,
    wt_dataset_path,
    detection_threshold_path,
    k,
    time_window,
)
from ibHH.InformationBasedHeavyHitter import InformationBasedHeavyHitter
from time import time

from metrics.metrics import true_positive_rate, false_positive_rate
from read_dns_queries import read_dns_queries
from utils import write_list_to_file, read_list_from_file

if __name__ == "__main__":

    df_global_allow_list = pd.read_csv(global_allowlist_path, header=None).rename(
        columns={0: "rank", 1: "domain"}
    )
    global_allow_list = set(df_global_allow_list["domain"].tolist())
    pt_allow_list = set(read_list_from_file(pt_path))
    allow_list = global_allow_list.union(pt_allow_list).difference(dns_exf_domains)
    detections = set()
    all_domains = set()
    filename = wt_dataset_path
    record_stream = read_dns_queries(filename)
    current_window = 0
    total_time = 0
    total_time_without_tldextract = 0
    ibhh = None
    with open(detection_threshold_path, "r") as f:
        detection_threshold = int(f.read())
    print(f"detection threshold: {detection_threshold}")
    extract = tldextract.TLDExtract(include_psl_private_domains=False)
    for record in record_stream:
        splitted = record.split(",")
        timestamp = int(splitted[0])
        dns_query = splitted[1]
        start_time = time()
        extracted = extract(dns_query)
        domain = extracted.registered_domain.lower()
        subdomain = extracted.subdomain
        all_domains.add(domain)
        start_time_without = time()
        if timestamp > current_window + time_window:
            ibhh = InformationBasedHeavyHitter(k=k)
            current_window = timestamp
        ibhh.add_pair(subdomain, domain)
        count = ibhh.count_domain_information(domain)
        if count > detection_threshold:
            detections.add(domain)
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

    detections = detections.difference(allow_list)
    print(f"num detections (after allow-listing):{len(detections)}")
    write_list_to_file(detections_path, list(detections))
    print(detections)
    tp = detections.intersection(dns_exf_domains)
    fp = detections.difference(dns_exf_domains)
    fn = dns_exf_domains.difference(tp)
    tn = all_domains.difference(tp).difference(fp)
    tpr = true_positive_rate(len(tp), len(fn))
    fpr = false_positive_rate(len(fp), len(tn))
    print(f"TP: {len(tp)} FP: {len(fp)}, total detections: {len(detections)}")
    print(f"TPR: {tpr}, FPR: {fpr}")
