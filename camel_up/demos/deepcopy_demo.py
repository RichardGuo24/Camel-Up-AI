from copy import deepcopy

if __name__ == "__main__":
    print("\ncopy() helps avoid object aliasing:")
    list1 = [1, 2, 3, 4, 5]
    print("\tOriginal list1:", list1)
    list2 = list1
    #list2 = list1.copy()
    print("\tOriginal list2:", list2)
    list2[0] += 3
    print("\tUpdated list2:", list2)
    print("\tlist1 is mutated via aliasing side effect:", list1)

    print("\ncopy()- protects top-level data structures, but shares references to nested objects (shallow copy)")
    list_of_lists1 = [[1], [2, 3], [4, 5]]
    print("\tOriginal list_of_lists1:", list_of_lists1)
    list_of_lists2 = list_of_lists1.copy()
    print("\tOriginal list_of_lists2:", list_of_lists2)
    list_of_lists2[0] = [300]
    list_of_lists2[1][0] = [888, 999]
    print("\tUpdated list_of_lists2:", list_of_lists2)
    print("\tlist_of_lists1 reflects aliasing side effect for nested objects in list_of_lists1:", list_of_lists1)

    print("\ndeepcopy() protects object references nested data structures:")
    list_of_lists1 = [[1], [2, 3], [4, 5]]
    print("\tOriginal list_of_lists1:", list_of_lists1)
    list_of_lists2 = deepcopy(list_of_lists1)
    print("\tOriginal list_of_lists2:", list_of_lists2)
    list_of_lists2[0] = [300]
    list_of_lists2[1][0] = [888, 999]
    print("\tUpdated list_of_lists2:", list_of_lists2)
    print("\tlist_of_lists1 is preserved via deepcopy:", list_of_lists1)
    print()

    

    


