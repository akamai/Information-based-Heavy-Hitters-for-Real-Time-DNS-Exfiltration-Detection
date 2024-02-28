raw_dataset_path = "DNS Exfiltration Dataset/dataset.csv"  # TODO: this assumes the "Ziza" dataset, change according to your dataset
preprocessed_dataset_path = "data/dataset_processed.csv"  # This file is generated by the code, you can change this as you'd like though
tuning_dataset_path = "data/tuning_dataset.csv"
pt_dataset_path = "data/pt_dataset.csv"
wt_dataset_path = "data/wt_dataset.csv"
detection_threshold_path = "detection_threshold.txt"
detections_path = "detections.txt"

dns_exf_domains = {
    "dnsresearch.ml",
    "e5.sk",
    "mcafee.com",
}


global_allowlist_path = ""  # TODO: fill this with the path to the global allow-list
pt_path = "data/allow_lists/pt_list.txt"

acceptable_fpr = 0.01  # Change this to be the desired acceptable FPR
k = 1000  # Size of the ibhh cache
time_window = 120000  # Detection time window, in milliseconds (for the reset mechanism)

# These are the columns in the Ziza dataset, they're not provided as header in the dataset's csv so in order to parse the rows I provide thses
columns = [
    "user_ip",
    "domain",
    "timestamp",
    "attack",
    "request",
    "len",
    "subdomains_count",
    "w_count",
    "w_max",
    "entropy",
    "w_max_ratio",
    "w_count_ratio",
    "digits_ratio",
    "uppercase_ratio",
    "time_avg",
    "time_stdev",
    "size_avg",
    "size_stdev",
    "throughput",
    "unique",
    "entropy_avg",
    "entropy_stdev",
]

columns_to_extract = ["timestamp", "request"]

tuning_cutoff_delta = 10
pt_cutoff_delta = 12
