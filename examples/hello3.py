"""Hello example using do-notation."""
from oslash import put_line, get_line, do, let

main = do(
    put_line("What is your name?"),
    let(name=get_line()),
    put_line("What is your age?"),
    let(age=get_line()),
    lambda e: put_line("Hello " + e.name + "!"),
    lambda e: put_line("You are " + e.age + " years old")
    )

if __name__ == "__main__":
    #print(main)
    main()
