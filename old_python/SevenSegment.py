class SevenSegmentNumber(object):
    """
    Digits are considered from left to right.
    The decimal point index is 

    """

    def __init__(self, num_digits):
        self.digits = list()
        i = 0
        while i <= num_digits:
            self.digits.append(None)


    def return_float(self):
        string = ""
        if self.digits:
            for digit in [ss_digit.return_str() for ss_digit in self.digits]:
                string+=digit
        else:
            raise RuntimeError("No digits provided.")

        return float(string)



class SevenSegmentDigit(object):
    """
        NUMBERING CONVENTION:

            000
         5       1
         5       1
            666
         4       2
         4       2
            333



    """
    def __init__(self):
        self.crd = [None, None, None, None, None, None, None]
        self.bools = [None, None, None, None, None, None, None]
        self.decimal = False

    def make_decimal(self, crd):
        self.crd = crd
        self.bools = True
        self.decimal = True

    def return_str(self):
        if not self.decimal:
            for boolean in self.bools:
                if boolean == None:
                    raise RuntimeError("Not enough segments specified in digit")

            if self.bools[0]\
            and self.bools[1]\
            and self.bools[2]\
            and self.bools[3]\
            and self.bools[4]\
            and self.bools[5]\
            and not self.bools[6]:
                return "0"

            elif not self.bools[0]\
            and self.bools[1]\
            and self.bools[2]\
            and not self.bools[3]\
            and not self.bools[4]\
            and not self.bools[5]\
            and not self.bools[6]:
                return "1"

            elif not self.bools[0]\
            and not self.bools[1]\
            and not self.bools[2]\
            and not self.bools[3]\
            and self.bools[4]\
            and self.bools[5]\
            and not self.bools[6]:
                return "1"

            elif self.bools[0]\
            and self.bools[1]\
            and not self.bools[2]\
            and self.bools[3]\
            and self.bools[4]\
            and not self.bools[5]\
            and self.bools[6]:
                return "2"

            elif self.bools[0]\
            and self.bools[1]\
            and self.bools[2]\
            and self.bools[3]\
            and not self.bools[4]\
            and not self.bools[5]\
            and self.bools[6]:
                return "3"

            elif not self.bools[0]\
            and self.bools[1]\
            and self.bools[2]\
            and not self.bools[3]\
            and not self.bools[4]\
            and self.bools[5]\
            and self.bools[6]:
                return "4"

            elif self.bools[0]\
            and not self.bools[1]\
            and self.bools[2]\
            and self.bools[3]\
            and not self.bools[4]\
            and self.bools[5]\
            and self.bools[6]:
                return "5"

            elif self.bools[0]\
            and not self.bools[1]\
            and self.bools[2]\
            and self.bools[3]\
            and self.bools[4]\
            and self.bools[5]\
            and self.bools[6]:
                return "6"

            elif self.bools[0]\
            and self.bools[1]\
            and self.bools[2]\
            and not self.bools[3]\
            and not self.bools[4]\
            and not self.bools[5]\
            and not self.bools[6]:
                return "7"

            elif self.bools[0]\
            and self.bools[1]\
            and self.bools[2]\
            and self.bools[3]\
            and self.bools[4]\
            and self.bools[5]\
            and self.bools[6]:
                return "8"

            elif self.bools[0]\
            and self.bools[1]\
            and self.bools[2]\
            and self.bools[3]\
            and not self.bools[4]\
            and self.bools[5]\
            and self.bools[6]:
                return "9"

            elif self.bools[0]\
            and self.bools[1]\
            and self.bools[2]\
            and not self.bools[3]\
            and not self.bools[4]\
            and self.bools[5]\
            and self.bools[6]:
                return "9"

            else:
                raise RuntimeError("Unrecognized Seven Segment Digit.")

        else:
            return "."
