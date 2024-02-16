import sys
from enigma.machine import EnigmaMachine
import pyAesCrypt
# import pikepdf
import shutil
import os


# setup machine according to specs from a daily key sheet:


class ENCRYPTOR:
	def __init__(self, dir_path) -> None:
		self.password = "iamadeveloper catronicprog venomraidershanslett thedev6413v1 point1"
		self.dir_path = dir_path

	def enigma_machine(self):
		machine = EnigmaMachine.from_key_sheet(
			rotors='II IV V',
			reflector='B',
			ring_settings=[23, 19, 7],
			plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')
		# set machine initial starting position
		machine.set_display('UPG')
		# decrypt the message key
		msg_key = machine.process_text('GRX')
		# decrypt the cipher text with the unencrypted message key
		msg_key = machine.set_display(msg_key)
		c = machine.process_text(self.password, replace_char='Z')
		return c
	
	def get_files(self):
		for abspath, folder, filenames in os.walk(self.dir_path):
			for filename in filenames:
				if filename.endswith(('.pdf')):
					try:
						print("Process ", os.path.join(abspath, filename))
						# self.decrypt_pdf(os.path.join(abspath, filename))
						# self.encrypt_pdf(os.path.join(abspath, filename))
					except Exception as e:
						print(e)
						continue

			
	def encrypt_pdf(self, path):
		try:
			password = self.enigma_machine()
			bufferSize = 64 * 1024
			with open(path, "rb") as fIn:
				with open(path + ".aes", "wb") as fOut:
					pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
			print(f"Encrypted {path}")
			os.remove(path)
		except Exception as e:
			print(e)
			
	def decrypt_pdf(self, path):
		try:
			password = self.enigma_machine()
			pdf = pikepdf.open(path, password=password)
			pdf.save("decrypt3.pdf")
			shutil.move("decrypt3.pdf", path)
			print("Decrypted", path)
		except Exception as e:
			print(e)
		# try:
		# 	pyAesCrypt.decryptFile(path, "test.pdf", password)
		# 	print(f"Decrypted {path}")
		# except Exception as e:
		# 	print(e)

		
# if __name__ == "__main__":
# 	path = sys.argv[1]
# 	main = ENCRYPTOR(r"" + path)
# 	main.get_files()
	# ciphertext = 'ZKDGHRWSTYV'
	# plaintext = machine.process_text(ciphertext)

	# print(plaintext)