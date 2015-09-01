class Employee(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        str = "Name: %s" % self.name
        str += "\nAge: %d" % self.age
        return str

    def __lt__(self, other):
        return (self.age < other.age)

if __name__ == '__main__':
    emp = Employee("Han", 30)
    emp2 = Employee("Chewie", 200)

    print emp
    print '%s is < than %s: %r' % (emp.name, emp2.name, emp < emp2)
