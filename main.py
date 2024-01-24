from Configuration import Configuration
from Plot import initialize_plot, update_gloabl_plot, freeze
from Rectangle import Rectangle as Rect
from Node import Node
from aStar import a_star
from time import time

cases = [
    (4,1),
    (4,5),
    (9,4),
    (3,5),
    (3,9),
    (1,4),
    (5,3),
    (4,1),
    (5,5),
    (7,2),
    (9,3),
    (6,2),
    (4,6),
    (6,3),
    (10,3),
    (6,3),
    # (6,3),
    # (10,3)
]

def main(
        cases: list[tuple[float, float]],
        container_size: tuple[float, float]=(15, 15),
        plotting: bool=True
        ):
    
    if plotting:
        cases_rects = [Rect((0, 0), x[0], x[1], False) for x in cases]
        config = Configuration(container_size, cases_rects, plot=False)
        initialize_plot(config, cases_rects, container_size)
        update_gloabl_plot(config)
    Configuration.plotting = plotting
    Node.all_rects = cases
    Node.con_sizes = container_size
    Node.con_area = container_size[0] * container_size[1]
    prime_node = Node([])
    best_config = a_star(prime_node)
    if plotting:
        freeze()
    else:
        cases_rects = [Rect((0, 0), x[0], x[1], False) for x in cases]
        initialize_plot(best_config, cases_rects, container_size)
        update_gloabl_plot(best_config)
        freeze()


if __name__ == "__main__":
    start = time()
    main(cases, plotting=True)
    end = time()
    print(end-start)