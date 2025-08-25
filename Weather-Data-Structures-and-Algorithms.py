import pandas as pd
from random import randint
import queue

class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        
    def insertAtBeginning(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node

    def insertAfter(self, prev_node, new_data):
        if prev_node is None:
            print("The given previous node must be in the LinkedList.")
            return
        new_node = Node(new_data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def insertAtEnd(self, new_data):
        new_node = Node(new_data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while (last.next):
            last = last.next

        last.next = new_node

    def deleteNode(self, position):
        if self.head is None:
            return
        temp = self.head
        if position == 0:
            self.head = temp.next
            temp = None
            return
        for i in range(position - 1):
            temp = temp.next
            if temp is None:
                break
        if temp is None:
            return
        if temp.next is None:
            return
        next_node = temp.next.next
        temp.next = next_node 

def quick_sort(array, key=None):
    if len(array) < 2:
        return array

    pivot = array[randint(0, len(array)-1)]
    low, same, high = [], [], []

    for item in array:
        a = item if key is None else item[key]
        p = pivot if key is None else pivot[key]
        if a < p:
            low.append(item)
        elif a == p:
            same.append(item)
        else:
            high.append(item)

    return quick_sort(low, key) + same + quick_sort(high, key)

def bubble_sort(array, key=None):
    n = len(array)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            a = array[j] if key is None else array[j][key]
            b = array[j + 1] if key is None else array[j + 1][key]
            if a > b:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break
    return array

def linear_search(array, target, key=None):
    results = []
    for item in array:
        value = item if key is None else item[key]
        if value == target:
            results.append(item)
    return results

def binary_search(arr, target, key=None, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low <= high:
        mid = (low + high) // 2
        mid_value = arr[mid] if key is None else arr[mid][key]
        if mid_value == target:
            return arr[mid]
        elif mid_value < target:
            return binary_search(arr, target, key, mid + 1, high)
        else:
            return binary_search(arr, target, key, low, mid - 1)
    return None

def view_data(linked_list, limit=10):
    current = linked_list.head
    count = 0
    if current is None:
        print("No records to display.")
        return

    while current and count < limit:
        print(current.data)
        current = current.next
        count += 1

    if current:
        print(f"...and more ({count}+ records)")

def main():
    try:
        df = pd.read_csv(r"C:\Users\salmaa\Downloads\weather.csv")
    except FileNotFoundError:
        print("Error: CSV file not found. Please check the file path.")
        return
    except Exception as e:
        print(f"Error while reading CSV: {e}")
        return

    weather_list = LinkedList()
    for record in df.to_dict('records'):
        weather_list.insertAtEnd(record)

    data_processing = queue.Queue()
    undo_stack = []
    redo_stack = []

    while True:
        print("\n=== Weather Data Processing System ===")
        print("1. View first 10 records")
        print("2. Quick Sort by column")
        print("3. Bubble Sort by column")
        print("4. Linear Search")
        print("5. Binary Search")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                view_data(weather_list)

            elif choice == "2":
                column = input("Enter column name to sort by: ").strip()
                if column not in df.columns:
                    raise ValueError("Invalid column name.")
                records = df.to_dict('records')
                sorted_records = quick_sort(records, key=column)
                print("Sorted (Quick Sort):")
                for r in sorted_records[:10]:
                    print(r)

            elif choice == "3":
                column = input("Enter column name to sort by: ").strip()
                if column not in df.columns:
                    raise ValueError("Invalid column name.")
                records = df.to_dict('records')
                sorted_records = bubble_sort(records, key=column)
                print("Sorted (Bubble Sort):")
                for r in sorted_records[:10]:
                    print(r)

            elif choice == "4":
                column = input("Enter column name to search by: ").strip()
                if column not in df.columns:
                    raise ValueError("Invalid column name.")
                target = input("Enter target value: ").strip()
                records = df.to_dict('records')
                results = linear_search(records, target, key=column)
                print(f"Found {len(results)} record(s):")
                for r in results[:10]:
                    print(r)

            elif choice == "5":
                column = input("Enter column name to search by: ").strip()
                if column not in df.columns:
                    raise ValueError("Invalid column name.")
                target = input("Enter target value: ").strip()
                records = df.to_dict('records')
                sorted_records = quick_sort(records, key=column)
                result = binary_search(sorted_records, target, key=column)
                if result:
                    print("Record found:", result)
                else:
                    print("Record not found.")

            elif choice == "6":
                print("Exiting program... ")
                break

            else:
                print("Invalid choice, please try again.")

        except ValueError as ve:
            print(f"Input Error: {ve}")
        except KeyError:
            print("Error: Column does not exist in the dataset.")
        except Exception as e:
            print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()
