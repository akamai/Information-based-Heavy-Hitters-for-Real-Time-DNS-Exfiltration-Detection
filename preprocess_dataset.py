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

from config import (
    columns,
    columns_to_extract,
    raw_dataset_path,
    preprocessed_dataset_path,
)


def preprocess(input_path, output_path, columns, columns_to_extract):
    df = pd.read_csv(input_path, header=None, names=columns)
    df[columns_to_extract].to_csv(output_path, index=False, header=True)


if __name__ == "__main__":
    preprocess(raw_dataset_path, preprocessed_dataset_path, columns, columns_to_extract)
