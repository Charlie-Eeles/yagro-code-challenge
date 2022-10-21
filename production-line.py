
from random import randint
from collections import deque

def production_line(line_length: int, steps: int):

    # This instantiates the workers as an array of arrays where:
        # every two arrays is a new 'step' of workers so workers[0] and workers[1] are opposite each other on the belt
        # the inner arrays represent their holding capacity so it's essentially [component grabbing hand, product building hand]
    workers = [[0,0] for i in range(line_length*2)]
    
    line = deque([0 for i in range(line_length)])

    finished_products = 0
    wasted_A_components = 0
    wasted_B_components = 0

    for step in range(steps):
        line.appendleft(randint(0,2))
        if line[-1] >=3: finished_products +=1
        if line[-1] ==1: wasted_A_components +=1
        if line[-1] ==2: wasted_B_components +=1
        line.pop()
        
        # print(line) 
        # ^ un-comment to see the 'belt'
        

        for worker in range(line_length):

            # >= 3 indicates that the item on the line is a product // 0 indicates an empty space on the belt
            if line[worker] < 3:

                both_workers = [workers[worker*2], workers[worker*2 +1]]

                action_taken = False

                def place_finished_product():
                    line[worker] += single_worker[1]
                    single_worker[1] = 0
                    return True

                def pick_up_component():
                    single_worker[0] += line[worker]
                    line[worker] = 0
                    return True

                def start_build():
                    single_worker[0] = 0
                    single_worker[1] = 2
                    line[worker] = 0
                    return True
                
                for single_worker in both_workers:
                    if action_taken is True: continue

                    # Checks what's in the 'component hand' -> 0 is nothing, 1 is component A, 2 is component B
                    match single_worker[0]:
                        case 0:
                            if single_worker[1] == 0 and line[worker] != 0:
                                action_taken = pick_up_component()
                                
                            if single_worker[1] >=6:
                                if line[worker] == 0:
                                    action_taken = place_finished_product()
                                    continue
                                action_taken = pick_up_component()

                        case 1:
                            if line[worker] == 2 and single_worker[1] == 0:
                                action_taken = start_build()

                            if single_worker[1] >=6 and line[worker] == 0:
                                action_taken = place_finished_product()

                        case 2:
                            if line[worker] == 1 and single_worker[1] == 0:
                                action_taken = start_build()

                            if single_worker[1] >=6 and line[worker] == 0:
                                action_taken = place_finished_product()

            if workers[worker*2][1] > 0 and workers[worker*2][1] < 8 : workers[worker*2][1] +=1
            if workers[worker*2+1][1] > 0 and workers[worker*2+1][1] < 8: workers[worker*2+1][1] +=1

        # print(workers)
        # print()
        # ^ un-comment to see workers

    
    print(f'{finished_products} finished products.')
    print(f'{wasted_A_components} A component(s) went through the production line without being picked up by anyone.')
    print(f'{wasted_B_components} B component(s) went through the production line without being picked up by anyone.')

    
production_line(3, 100)

# NB:
# This solution was made under the assumption that the workers could only put finished products on empty spaces on the belt
# but they could pick one component up if they were finished building the product.