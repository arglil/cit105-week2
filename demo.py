from functions import (
    celsius_to_fahrenheit,
    line_total,
    initials,
    is_valid_url,
    truncate,
    safe_filename,
)


print("Demonstration of functions.py")

# celsius_to_fahrenheit
try:
    print("celsius_to_fahrenheit(25) ->", celsius_to_fahrenheit(25))
except (TypeError, ValueError) as e:
    print("celsius_to_fahrenheit valid test raised:", e)

try:
    print("celsius_to_fahrenheit('25') ->", celsius_to_fahrenheit('25'))
except (TypeError, ValueError) as e:
    print("celsius_to_fahrenheit invalid test raised:", e)

# line_total
try:
    print("line_total(12.5, 4) ->", line_total(12.5, 4))
except (TypeError, ValueError) as e:
    print("line_total valid test raised:", e)

try:
    print("line_total(12.5, -2) ->", line_total(12.5, -2))
except (TypeError, ValueError) as e:
    print("line_total invalid test raised:", e)

# initials
try:
    print("initials('Luis De Leon') ->", initials("Luis De Leon"))
except (TypeError, ValueError) as e:
    print("initials valid test raised:", e)

try:
    print("initials(123) ->", initials(123))
except (TypeError, ValueError) as e:
    print("initials invalid test raised:", e)

# is_valid_url
try:
    print("is_valid_url('https://google.com/') ->", is_valid_url("https://google.com/"))
except (TypeError, ValueError) as e:
    print("is_valid_url valid test raised:", e)

try:
    print("is_valid_url('   ') ->", is_valid_url("   "))
except (TypeError, ValueError) as e:
    print("is_valid_url invalid test raised:", e)

# truncate
try:
    print("truncate('This is a long sentence', 20) ->", truncate("This is a long sentence", 20))
except (TypeError, ValueError) as e:
    print("truncate valid test raised:", e)

try:
    print("truncate('hello', -5) ->", truncate("hello", -5))
except (TypeError, ValueError) as e:
    print("truncate invalid test raised:", e)

# safe_filename
try:
    print("safe_filename('My File 2024?') ->", safe_filename("My File 2024?"))
except (TypeError, ValueError) as e:
    print("safe_filename valid test raised:", e)

try:
    print("safe_filename(42) ->", safe_filename(42))
except (TypeError, ValueError) as e:
    print("safe_filename invalid test raised:", e)
