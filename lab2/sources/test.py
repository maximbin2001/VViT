from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

key = env.str("KEY")  # Забираем значение типа str

print(key)