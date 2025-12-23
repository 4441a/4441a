import argparse
import math

def parse_args():
    parser = argparse.ArgumentParser(description='Displays a table for the formula a_n=((n*2)**p)+(n*3)**q')
    parser.add_argument('n', type=int, help='max n value for the formula')
    parser.add_argument('p', type=float, help='p value for the formula')
    parser.add_argument('q', type=float, help='q value for the formula')
    args = parser.parse_args()
    return args

def formula(n, p, q):
    a_n = ((n * 2) ** p) + (n * 3) ** q
    return a_n

def print_table(n, p, q):
    for i in range(0, n+1):
        a_i = formula(i, p, q)
        
        # print indexes as columns and a values as rows
        print("{:^3} {:^10}".format(i, int(a_i)), end = ' ')
        
        # print new line after every 10 values
        if (i+1) % 10 == 0 and i+1 != n+1:
            print('\n')

    # print max line for better readability
    print("\n{} |".format("-" * (n*3 + 19)))
    
    # calculate max_a
    max_a = formula(n, p, q)
    
    # calculate m_a
    p = float(p)
    q = float(q)
    m_a = int((2**(p)) * (3**q) * (n+1)) -1
    print("\nMax a_n: {:^10} for n >= {}".format(max_a, m_a))
    print("")

if __name__ == "__main__":
    args = parse_args()
    print_table(args.n, args.p, args.q)
