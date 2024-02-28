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
from datetime import timedelta
from config import (
    preprocessed_dataset_path,
    tuning_dataset_path,
    wt_dataset_path,
    pt_dataset_path,
    tuning_cutoff_delta,
    pt_cutoff_delta,
)


def load_dataframe(path, columns=None):
    if columns:
        return pd.read_csv(path, usecols=columns)
    return pd.read_csv(path)


def write_df(df, path, columns=None):
    if columns:
        df[columns].to_csv(path, index=False)
    else:
        df.to_csv(path, index=False)


if __name__ == "__main__":
    df = load_dataframe(preprocessed_dataset_path)
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    tune_cutoff_date = df["date"].min() + timedelta(hours=tuning_cutoff_delta)
    peace_time_cutoff_date = df["date"].min() + timedelta(hours=pt_cutoff_delta)

    df_tune = df[df["date"] < tune_cutoff_date]
    df_pt = df[(df["date"] >= tune_cutoff_date) & (df["date"] < peace_time_cutoff_date)]
    df_wt = df[df["date"] > peace_time_cutoff_date]

    df_tune.sort_values(by="timestamp").to_csv(tuning_dataset_path, index=False)
    df_pt.sort_values(by="timestamp").to_csv(pt_dataset_path, index=False)
    df_wt.sort_values(by="timestamp").to_csv(wt_dataset_path, index=False)
