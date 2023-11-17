from keystone import *


def assemble_asm(asm_code):
    try:
        ks = Ks(KS_ARCH_X86, KS_MODE_64)  # 设置目标架构为 x86_64
        encoding, _ = ks.asm(asm_code)
        return bytes(encoding)
    except KsError as e:
        print(f"Assembly failed: {e}")
        return None


def main():
    asm_code = "mov rax, 0x1234567890ABCDEF"
    bytecode = assemble_asm(asm_code)

    if bytecode:
        print("Assembly succeeded:")
        print(bytecode)
        print(list(bytecode))
        list(bytecode)
        hex_bytecode = ' '.join([hex(byte) for byte in bytecode])
        print(hex_bytecode)


if __name__ == '__main__':
    main()
