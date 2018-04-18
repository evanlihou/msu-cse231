
##
## Class PetError -- complete
##

class PetError( ValueError ):
    
    pass


class Pet(object):
    def __init__(self, species=None, name=""):
        if species.lower() in ['dog', 'cat', 'horse', 'gerbil', 'hamster', 'ferret']:
            self.species_str = species.title()
            self.name_str = name.title()
        else:
            raise PetError()

    def __str__(self):
        if self.name_str != "":
            result_str = "Species of {:s}, named {:s}".format(
                self.species_str, self.name_str)
        else:
            result_str = "Species of {:s}, unnamed".format(
                self.species_str)
        return result_str


class Dog(Pet):
    def __init__(self, name="", chases="cats"):
        Pet.__init__(self, "dog", name)
        self.chases = chases.title()

    def __str__(self):
        return Pet.__str__(self) + ", chases {:s}".format(self.chases)


class Cat( Pet ):
    def __init__(self, name="", hates="dogs"):
        Pet.__init__(self, "cat", name)
        self.hates = hates

    def __str__(self):
        return Pet.__str__(self) + ", hates {:s}".format(self.hates)
