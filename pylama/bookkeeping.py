
class BookKeeping(object):

    labels = {}
    blocks = {}
    is_used = False
    section_compensated = False

    @staticmethod
    def add_label(label, block):
        if label in BookKeeping.labels:
            return
        if block in BookKeeping.blocks:
            BookKeeping.labels[label] = (block, BookKeeping.blocks[block]+1)
            BookKeeping.blocks[block] += 1
        else:
            BookKeeping.labels[label] = (block, 0)
            BookKeeping.blocks[block] = 0
        if block == "section":
            # TODO: counter should be reset for nested sections
            for nesting in range(1, 5):
                subsub = "sub"*nesting + "section"
                if subsub in BookKeeping.blocks:
                    BookKeeping.blocks[subsub] = -1
            if BookKeeping.section_compensated:
                BookKeeping.blocks["section"] -= 1
                BookKeeping.section_compensated = False
        elif not BookKeeping.section_compensated and "subsection" in block:
            BookKeeping.blocks["section"] += 1
            BookKeeping.section_compensated = True


    @staticmethod
    def ref(label):
        if label not in BookKeeping.labels:
            return None
        (block, number) = BookKeeping.labels[label]
        return number+1
