
class BookKeeping(object):

    labels = {}
    blocks = {}
    is_used = False

    @staticmethod
    def add_label(label, block):
        if label in BookKeeping.labels:
            return
        if block in BookKeeping.blocks:
            BookKeeping.labels[label] = (block, BookKeeping.blocks[block]+1)
            BookKeeping.blocks[block] += 1
        else:
            BookKeeping.labels[label] = (block, 1)
            BookKeeping.blocks[block] = 1
        if block == "section":
            for nesting in range(1, 5):
                subsub = "sub"*nesting + "section"
                if subsub in BookKeeping.blocks:
                    BookKeeping.blocks[subsub] = -1

    @staticmethod
    def ref(label):
        if label not in BookKeeping.labels:
            return None
        (block, number) = BookKeeping.labels[label]
        return number
