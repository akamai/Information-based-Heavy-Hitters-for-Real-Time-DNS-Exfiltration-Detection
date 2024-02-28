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

from WHLL import WeightedHyperLogLog
import mmh3


def get_int_value(pair):
    return pair[1][1]


class InformationBasedHeavyHitter(object):
    def __init__(self, k, threshold=2 ** 128):
        self.information_counters = {}
        self.seeds = {}
        self.threshold = threshold
        self.k = k

    def add_pair(self, subdomain: str, domain: str):
        hash_value = mmh3.hash128(subdomain + domain)
        if domain in self.information_counters:
            self.information_counters[domain].add(subdomain)
            if hash_value < self.seeds[domain]:
                self.seeds[domain] = hash_value
        elif hash_value < self.threshold:
            self.information_counters[domain] = WeightedHyperLogLog(p=12, sparse=False)
            self.information_counters[domain].add(subdomain)

            self.seeds[domain] = hash_value
            if len(self.seeds) > self.k:
                max_seed_domain = max(self.seeds, key=self.seeds.get)
                self.threshold = self.seeds[max_seed_domain]
                del self.information_counters[max_seed_domain]
                del self.seeds[max_seed_domain]

    def count_cache_information(self):
        return [
            (domain, self.information_counters[domain].cardinality())
            for domain in self.information_counters
        ]

    def count_domain_information(self, domain):
        return (
            self.information_counters[domain].cardinality()
            if domain in self.information_counters
            else 0
        )
