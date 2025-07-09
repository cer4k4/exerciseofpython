def bucket_sort(arr):
    if not arr or len(arr) <= 1:
        return arr

    num_buckets = len(arr)
    
    buckets = [[] for _ in range(num_buckets)]

    max_val = max(arr)

    for num in arr:
        bucket_index = int((num / (max_val + 1)) * num_buckets)
        buckets[bucket_index].append(num)


    for i in range(num_buckets):
        buckets[i].sort()


    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)

    return sorted_arr


data_integers = [12, 5, 8, 20, 3, 15, 7]
sorted_integers = bucket_sort(data_integers)
print(f"Original integer array: {data_integers}")
print(f"Sorted integer array: {sorted_integers}")