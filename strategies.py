
BASIC_STRAT = {
    "hard": {
        9: {2: "hit", 3: "double", 4: "double", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        10: {2: "hit", 3: "double", 4: "double", 5: "double", 6: "double", 7: "double", 8: "double", 9: "double", 10: "hit", 1: "hit"},
        11: {2: "double", 3: "double", 4: "double", 5: "double", 6: "double", 7: "double", 8: "double", 9: "double", 10: "double", 1: "double"},
        12: {2: "hit", 3: "hit", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        13: {2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        14: {2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        15: {2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        16: {2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"}
    },
    "soft": {
        13: {2: "hit", 3: "hit", 4: "hit", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        14: {2: "hit", 3: "hit", 4: "hit", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        15: {2: "hit", 3: "hit", 4: "double", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        16: {2: "hit", 3: "hit", 4: "double", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        17: {2: "hit", 3: "double", 4: "double", 5: "double", 6: "double", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        18: {2: "double", 3: "double", 4: "double", 5: "double", 6: "double", 7: "stand", 8: "stand", 9: "hit", 10: "hit", 1: "hit"},
        19: {2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "double", 9: "stand", 10: "stand", 1: "stand"},
        20: {2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "double", 9: "stand", 10: "stand", 1: "stand"},
        20: {2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "stand", 9: "stand", 10: "stand", 1: "stand"},
        21: {2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "stand", 9: "stand", 10: "stand", 1: "stand"}

    },
    "pair": {
        2: {2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        3: {2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        4: {2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        5: {2: "hit", 3: "double", 4: "double", 5: "double", 6: "double", 7: "double", 8: "double", 9: "double", 10: "hit", 1: "hit"},
        6: {2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "hit", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        7: {2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "hit", 9: "hit", 10: "hit", 1: "hit"},
        8: {2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "split", 9: "split", 10: "split", 1: "split"},
        9: {2: "split", 3: "split", 4: "split", 5: "split", 6: "hit", 7: "split", 8: "split", 9: "stand", 10: "stand", 1: "stand"},
        10: {2: "stand", 3: "stand", 4: "stand", 5: "stand", 6: "stand", 7: "stand", 8: "stand", 9: "stand", 10: "stand", 1: "stand"},
        1: {2: "split", 3: "split", 4: "split", 5: "split", 6: "split", 7: "split", 8: "split", 9: "hit", 10: "hit", 1: "hit"}
    }
}

if __name__ == "__main__":

    list = [1,1,1,1]

    list.insert(1, 2)

    print(list)

