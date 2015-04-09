from oslash import put_line, get_line

main = put_line("What is your name?") | (lambda _:
        get_line() | (lambda name:
        put_line("What is your age?") | (lambda _:
        get_line() | (lambda age:
        put_line("Hello " + name + "!") | (lambda _:
        put_line("You are " + age + " years old"))))))

if __name__ == "__main__":
    main()
