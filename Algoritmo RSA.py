import random

def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def euclides_extendido(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = euclides_extendido(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def es_primo(n, k=40):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generar_primo(bits):
    while True:
        num = random.getrandbits(bits)
        if es_primo(num):
            return num

def generar_claves(bits=512):
    p = generar_primo(bits // 2)
    q = generar_primo(bits // 2)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537
    if mcd(e, phi_n) != 1:
        raise ValueError("e no es coprimo con φ(n)")

    _, d, _ = euclides_extendido(e, phi_n)
    d = d % phi_n
    if d < 0:
        d += phi_n

    return (e, n), (d, n), (p, q)

def exponenciacion_rapida(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def cifrar_numero(mensaje_num, clave_publica):
    e, n = clave_publica
    return exponenciacion_rapida(mensaje_num, e, n)

def descifrar_numero(mensaje_cifrado, clave_privada):
    d, n = clave_privada
    return exponenciacion_rapida(mensaje_cifrado, d, n)

def descifrar_crt(cifrado, clave_privada, p, q):
    d, n = clave_privada
    dp = d % (p - 1)
    dq = d % (q - 1)
    q_inv = euclides_extendido(q, p)[1] % p

    m1 = exponenciacion_rapida(cifrado, dp, p)
    m2 = exponenciacion_rapida(cifrado, dq, q)

    h = (q_inv * (m1 - m2)) % p
    return (m2 + h * q) % n

def mensaje_a_numeros(mensaje):
    return [ord(c) for c in mensaje]

def numeros_a_mensaje(numeros):
    return ''.join([chr(n) for n in numeros])

def cifrar_mensaje(mensaje, clave_publica):
    bloques = mensaje_a_numeros(mensaje)
    bloques_cifrados = [cifrar_numero(bloque, clave_publica) for bloque in bloques]
    return bloques_cifrados

def descifrar_mensaje(bloques_cifrados, clave_privada, p=None, q=None):
    if p and q:
        bloques_descifrados = [descifrar_crt(bloque, clave_privada, p, q) for bloque in bloques_cifrados]
    else:
        bloques_descifrados = [descifrar_numero(bloque, clave_privada) for bloque in bloques_cifrados]
    return numeros_a_mensaje(bloques_descifrados)

def menu():
    print("\n--- Menú de RSA ---")
    print("1. Generar claves RSA")
    print("2. Cifrar un mensaje")
    print("3. Descifrar un mensaje")
    print("4. Salir")
    return input("Elige una opción: ")

def main():
    clave_publica = None
    clave_privada = None
    p, q = None, None
    mensaje_cifrado = None

    while True:
        opcion = menu()

        if opcion == "1":
            bits = int(input("Introduce el tamaño de las claves (ej. 512, 1024): "))
            clave_publica, clave_privada, (p, q) = generar_claves(bits)
            print(f"\nClaves generadas con éxito:")
            print(f"Clave pública (e, n): {clave_publica}")
            print(f"Clave privada (d, n): {clave_privada}")

        elif opcion == "2":
            if clave_publica is None:
                print("Primero debes generar las claves.")
            else:
                mensaje = input("Introduce el mensaje a cifrar: ")
                mensaje_cifrado = cifrar_mensaje(mensaje, clave_publica)
                print(f"Mensaje cifrado: {mensaje_cifrado}")

        elif opcion == "3":
            if clave_privada is None or mensaje_cifrado is None:
                print("Primero debes generar las claves y cifrar un mensaje.")
            else:
                mensaje_descifrado = descifrar_mensaje(mensaje_cifrado, clave_privada, p, q)
                print(f"Mensaje descifrado: {mensaje_descifrado}")

        elif opcion == "4":
            print("Chao")
            break

        else:
            print("Opción no válida, por favor elige de nuevo.")

if __name__ == "__main__":
    main()
