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

from tldextract import TLDExtract
from config import pt_dataset_path, pt_path, detection_threshold_path
from ibHH.InformationBasedHeavyHitter import InformationBasedHeavyHitter
from time import time
from read_dns_queries import read_dns_queries
from utils import write_list_to_file

if __name__ == "__main__":
    filename = pt_dataset_path
    query_stream = read_dns_queries(filename)
    k = 1000
    current_window = 0
    time_window = 120000
    total_time = 0
    total_time_without_tldextract = 0
    ibhh = None
    with open(detection_threshold_path, "r") as f:
        detection_threshold = int(f.read())
    print(detection_threshold)
    pt_allow_list = set()
    extract = TLDExtract(include_psl_private_domains=False)
    for query in query_stream:
        comma_split = query.split(",")
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
        if count > detection_threshold:
            pt_allow_list.add(domain)
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
    write_list_to_file(pt_path, pt_allow_list)
