
import sys
import os

# Функція сортування вставками (для підмасивів розміром <= 3)
def insertion_sort(arr, low, high, comp):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while True:
            comp[0] += 1  # рахунок порівняння перед умовою
            if j >= low and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key

# Алгоритм 1: Класичний QuickSort
def partition1_mod(arr, low, high, comp, first_call=False):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        comp[0] += 2
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    if not first_call and (high - low) >= 4:
        comp[0] += 1
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort1(arr, low, high, comp, first_call=False):
    if low < high:
        p = partition1_mod(arr, low, high, comp, first_call)
        quicksort1(arr, low, p - 1, comp, False)
        quicksort1(arr, p + 1, high, comp, False)


# Алгоритм 2: QuickSort з медіаною трьох
def quicksort2(arr, low, high, comp):
    if high - low + 1 > 3:
        mid = (low + high) // 2
        triple = [arr[low], arr[mid], arr[high]]
        med = sorted(triple)[1]
        if med == arr[low]:
            arr[low], arr[high] = arr[high], arr[low]
        elif med == arr[mid]:
            arr[mid], arr[high] = arr[high], arr[mid]
        p = partition1_standard(arr, low, high, comp)
        quicksort2(arr, low, p - 1, comp)
        quicksort2(arr, p + 1, high, comp)
        comp[0] += 1
    else:
        insertion_sort(arr, low, high, comp)

# Стандартна функція розбиття для алгоритму 2 (підрахунок 1 порівняння за ітерацію)
def partition1_standard(arr, low, high, comp):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        comp[0] += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    comp[0] += 1
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Алгоритм 3: QuickSort з трьома опорними елементами
def quicksort3(arr, low, high, comp):
    if high - low + 1 > 3:
        pivots = [arr[low], arr[low + 1], arr[high]]
        p_sorted = sorted(pivots)
        p1, p2, p3 = p_sorted[0], p_sorted[1], p_sorted[2]
        region1 = []
        region2 = []
        region3 = []
        region4 = []
        for k in range(low + 2, high):
            comp[0] += 1
            if arr[k] < p1:
                region1.append(arr[k])
            else:
                comp[0] += 1
                if arr[k] < p2:
                    region2.append(arr[k])
                else:
                    comp[0] += 1
                    if arr[k] < p3:
                        region3.append(arr[k])
                    else:
                        region4.append(arr[k])
        new_sub = region1 + [p1] + region2 + [p2] + region3 + [p3] + region4
        arr[low:high + 1] = new_sub
        q1 = low + len(region1)
        q2 = q1 + 1 + len(region2)
        q3 = q2 + 1 + len(region3)
        quicksort3(arr, low, q1 - 1, comp)
        quicksort3(arr, q1 + 1, q2 - 1, comp)
        quicksort3(arr, q2 + 1, q3 - 1, comp)
        quicksort3(arr, q3 + 1, high, comp)
    else:
        insertion_sort(arr, low, high, comp)

# Головна функція
def main():
    if len(sys.argv) != 2:
        print("Usage: {} <input_filename>".format(sys.argv[0]))
        sys.exit(1)

    input_filename = sys.argv[1]
    try:
        with open(input_filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print("Error reading file:", e)
        sys.exit(1)

    try:
        n = int(lines[0])
    except ValueError:
        print("Перший рядок повинен містити число (розмір масиву)")
        sys.exit(1)
    try:
        arr_original = [int(x) for x in lines[1:n + 1]]
    except Exception as e:
        print("Помилка перетворення елементів масиву:", e)
        sys.exit(1)

    arr1 = arr_original.copy()
    arr2 = arr_original.copy()
    arr3 = arr_original.copy()

    comp1 = [0]
    comp2 = [0]
    comp3 = [0]

    # Виконуємо алгоритми:
    quicksort1(arr1, 0, n - 1, comp1, first_call=True)
    quicksort2(arr2, 0, n - 1, comp2)
    quicksort3(arr3, 0, n - 1, comp3)

    result_line = f"{comp1[0]} {comp2[0]} {comp3[0]}"

    base_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    output_filename = base_name + "_output.txt"

    try:
        with open(output_filename, "w") as f:
            f.write(result_line)
    except Exception as e:
        print("Error writing output file:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
