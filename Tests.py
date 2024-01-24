import random
from aStar import run, a_star, a_star_time_capture
from matplotlib import pyplot as plt

ELEMENTS_RATIO = 1.3
ELEMENTS_NUMBER = 16
MAX_EL_LEN_RATIO = 0.7
MIN_EL_LEN_RATIO = 0.3

def set_seed(rand_seed: int):
    random.seed(rand_seed)

def get_seed(file_name: str="seed.txt") -> int:
    rand_seed = 42
    try:
        with open(file_name, "r") as file:
            line = file.readline()
            rand_seed = int(line)
    except Exception:
        print(f"Could not read random seed from file: {file_name}")
    return rand_seed

def reduce_sizes(target, elements):
    min_el_size = 2
    while target < sum([el[0] * el[1] for el in elements]):
        random_index = random.randint(0, len(elements) - 1)
        temp_elements = elements[random_index]
        if max(temp_elements) > min_el_size and min(temp_elements) > min_el_size:
            reduced = random.choice([(min(temp_elements), max(temp_elements) -1), (min(temp_elements) -1, max(temp_elements))])
            elements[random_index] = reduced

def generate_float_tuples(num_tuples, con_len, max_elem_ratio, min_elem_ratio):
    tuples = []
    edges = (con_len*min_elem_ratio, con_len*max_elem_ratio)
    for i in range(num_tuples):
        float1 = random.uniform(edges[0], edges[1])
        float2 = random.uniform(edges[0], edges[1])
        tuples.append((float1, float2))
    return tuples

def generate_int_tuples(num_tuples, con_len, max_elem_ratio, min_elem_ratio):
    tuples = []
    edges = (int(con_len*min_elem_ratio), int(con_len*max_elem_ratio))
    for _ in range(num_tuples):
        int1 = random.randint(edges[0], edges[1])
        int2 = random.randint(edges[0], edges[1])
        tuples.append((int1, int2))
    return tuples

def add_dictionaries(time_dict: dict, temp_time_dict: dict, number_of_founds: dict):
    for key, val in temp_time_dict.items():
        time_dict[key] += val
        if val > 0:
            number_of_founds[key] += 1

def get_stats(times_dict: dict, number_dict: dict) -> tuple[list, list]:
    times = []
    values = []
    for quality, number in number_dict.items():
        if number > 0:
            values.append(number)
            times.append(times_dict[quality] / number)
    return values, times


def float_int_comparation_test():
    tests_num = 2
    int_dict_times = {i: 0 for i in range(ELEMENTS_NUMBER + 1)}
    float_dict_times = {i: 0 for i in range(ELEMENTS_NUMBER + 1)}
    container_size: tuple[float, float]=(15, 15)
    number_of_found_ints = {i: 0 for i in range(ELEMENTS_NUMBER)}
    number_of_found_floats = {i: 0 for i in range(ELEMENTS_NUMBER)}
    for i in range(tests_num):
        set_seed(get_seed() + i)
        float_elem = generate_float_tuples(ELEMENTS_NUMBER, container_size[1], MAX_EL_LEN_RATIO, MIN_EL_LEN_RATIO)
        int_elem = generate_int_tuples(ELEMENTS_NUMBER, container_size[1], MAX_EL_LEN_RATIO, MIN_EL_LEN_RATIO)
        reduce_sizes(container_size[0] * container_size[1] *ELEMENTS_RATIO, float_elem)
        reduce_sizes(container_size[0] * container_size[1]*ELEMENTS_RATIO, int_elem)
        config, times_float = run(a_star_time_capture, float_elem, container_size, False, False)
        if config is not None:
            add_dictionaries(float_dict_times, times_float, number_of_found_floats)
        config, temp_int_dict = run(a_star_time_capture, int_elem, container_size, False, False)
        if config is not None:
            add_dictionaries(int_dict_times, temp_int_dict, number_of_found_ints)

    values_ints, times_ints = get_stats(int_dict_times, number_of_found_ints)
    values_floats, times_floats = get_stats(float_dict_times, number_of_found_floats)
    plt.plot(times_ints, values_ints, label="integers")
    plt.plot(times_floats, values_floats, label="floats")
    plt.legend()
    plt.title('Values found in time')
    plt.xlabel('mean of times')
    plt.ylabel('values')
    plt.show()





def float_int_quality_test():
    tests_num = 10
    int_sum = 0
    float_sum = 0
    container_size: tuple[float, float]=(15, 15)
    for i in range(tests_num):
        set_seed(get_seed() + i)
        float_elem = generate_float_tuples(ELEMENTS_NUMBER, container_size[1], MAX_EL_LEN_RATIO, MIN_EL_LEN_RATIO)
        int_elem = generate_int_tuples(ELEMENTS_NUMBER, container_size[1], MAX_EL_LEN_RATIO, MIN_EL_LEN_RATIO)
        reduce_sizes(container_size[0] * container_size[1] *ELEMENTS_RATIO, float_elem)
        reduce_sizes(container_size[0] * container_size[1]*ELEMENTS_RATIO, int_elem)
        config = run(a_star, float_elem, container_size, False, False)
        if config is not None:
            float_sum += len(config.packed_rects)
        config = run(a_star, int_elem, container_size, False, False)
        if config is not None:
            int_sum += len(config.packed_rects)
    print(f"Mean for ints: {int_sum/tests_num}")
    print(f"Mean for floats: {float_sum/tests_num}")




if __name__ == "__main__":
    float_int_comparation_test()