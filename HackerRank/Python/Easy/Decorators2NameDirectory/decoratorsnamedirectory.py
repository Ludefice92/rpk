import operator

def person_lister(f):
    def inner(people):
        # complete the function
        people_groups = sorted(people, key=lambda person: int(person[2]))
        return [f(person) for person in people_groups]
    return inner

@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    people = [input().split() for i in range(int(input()))]
    print(*name_format(people), sep='\n')