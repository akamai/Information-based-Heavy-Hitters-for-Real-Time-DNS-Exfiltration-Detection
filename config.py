# Mostly path values, modify them according to your environment as needed

original_path = "dataset_without_domain_subdomain.csv"

preprocessed_dataset_path = "data/dataset_processed.csv"
tuning_dataset_path = "data/tuning_dataset.csv"
pt_dataset_path = "data/pt_dataset.csv"
wt_dataset_path = "data/test_dataset.csv"

dns_exf_domains = {"dnsresearch.ml", "e5.sk", "mcafee.com"}

detection_threshold_path = "detection_threshold.txt"
detections_path = "detections.pkl"

tranco_path = "data/allow_lists/tranco.csv"
pt_path = "data/allow_lists/pt_list.txt"  # "peace_time.pkl"

acceptable_fpr = 0.01
k = 1000
detection_window = "2T"

# These are the columns in the Ziza dataset, they're not provided as header in the dataset's csv
columns = ["user_ip", "domain", "timestamp", "attack", "request", "len", "subdomains_count", "w_count", "w_max",
           "entropy", "w_max_ratio", "w_count_ratio", "digits_ratio", "uppercase_ratio", "time_avg", "time_stdev",
           "size_avg", "size_stdev", "throughput", "unique", "entropy_avg", "entropy_stdev"]

columns_to_extract = ["timestamp", "request"]  # ["timestamp", "request", "domain"]

tuning_cutoff_delta = 10
pt_cutoff_delta = 12
