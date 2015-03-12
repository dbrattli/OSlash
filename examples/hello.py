from oslash import put, get

main = put("What is your name?") >> (lambda _:
    get() >> (lambda name:
    put("What is your age?") >> (lambda _:
    get() >> (lambda age:
    put("Hello " + name + "!") >> (lambda _:
    put("You are " + age + " years old"))))))

if __name__ == "__main__":
    main()
