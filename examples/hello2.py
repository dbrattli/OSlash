"""Hello example as expression tree."""
from oslash import Put, Get, Return, Unit

main = Put("What is your name?",
         Get(lambda name:
           Put("What is your age?",
             Get(lambda age:
               Put("Hello " + name + "!",
                 Put("You are " + age + " years old",
                   Return(Unit)
                 )
               )
             )
           )
         )
       )

if __name__ == "__main__":
    print(main)
