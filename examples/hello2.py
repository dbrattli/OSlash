from oslash import Put, Get, IOAction

main = Put("What is your name?",
         Get(lambda name:
           Put("What is your age?",
             Get(lambda age:
               Put("Hello " + name + "!",
                 Put("You are " + age + " years old",
                   IOAction(())
                 )
               )
             )
           )
         )
       )

if __name__ == "__main__":
    main()
