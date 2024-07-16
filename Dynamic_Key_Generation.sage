import hashlib
import numpy as np
import sympy
def Inverse_Element_Ring(N):
	Inverse_Element_Table=[]
	for tt in range(1,N-1):
		if gcd(tt,N)==1:
			Inverse_Element_Table.append(tt)
	return Inverse_Element_Table
def Hash_DK_Generator(DK,n):
	Hash_DK_Vect=[]
	DK_String='0'
	for tt in range(0,len(DK)):
		DK_String=DK_String+str(DK[tt])
	Hash_DK_Vect.append(hashlib.sha256(DK_String.encode()).hexdigest())
	for tt in range(0,n):
		test_hash=Hash_DK_Vect[tt]
		Hash_DK_Vect.append(hashlib.sha256(test_hash.encode()).hexdigest())
	return Hash_DK_Vect
def Add_Round_Keys_Generation(DK_Hash_Output_Bits,l,Inverse_Element_Ring_Table):
	Len_Inverse_Element_Ring_Bits=ceil(log(len(Inverse_Element_Ring_Table),2))
	DK_Hash_Output_Bits_Final_Add_Round=DK_Hash_Output_Bits
	if l*9*Len_Inverse_Element_Ring_Bits>len(DK_Hash_Output_Bits):
		len_intermediate=l*9*Len_Inverse_Element_Ring_Bits-len(DK_Hash_Output_Bits)
		for tt in range(0,ceil(len_intermediate/len(DK_Hash_Output_Bits))):
			DK_Hash_Output_Bits_Final_Add_Round=DK_Hash_Output_Bits_Final_Add_Round+DK_Hash_Output_Bits
	Add_Round_Key_Vector=[]	
	for tt in range(0,l):
		test=[]
		for ii in range(9*tt,9*(tt+1)):
			test_bits='0'
			for kk in range(ii*(Len_Inverse_Element_Ring_Bits-1),ii*(Len_Inverse_Element_Ring_Bits-1)+(Len_Inverse_Element_Ring_Bits-1)):
				test_bits=test_bits+DK_Hash_Output_Bits_Final_Add_Round[kk]
			test.append(Inverse_Element_Ring_Table[mod(int(test_bits,2),len(Inverse_Element_Ring_Table))])
		Add_Round_Key_Vector.append(matrix(np.reshape(test,(3,3))))
	return 	Add_Round_Key_Vector
def Inverse_Add_Round_Key_Generation(Add_Round_Key_Vector,N):
	Add_Round_Key_Vect_Inverse=[]
	for tt in range(0,len(Add_Round_Key_Vector)):
		Key_Matrix=Add_Round_Key_Vector[tt]
		Key_Matrix_Inverse=matrix(3,3)
		for ii in range(0,3):
			for jj in range(0,3):
				Key_Matrix_Inverse[ii,jj]=pow(Key_Matrix[ii,jj],-1,N)
		Add_Round_Key_Vect_Inverse.append(Key_Matrix_Inverse)
	return Add_Round_Key_Vect_Inverse

def rc4keyperm(key, lenPbox):
	Pbox_temp= np.empty([lenPbox], dtype=int)
	lenkey=len(key)
	for i in range(lenPbox):
		Pbox_temp[i]=i
	j0=1
	for i0 in range(lenPbox):
		j0=(j0+Pbox_temp[i0] + Pbox_temp[j0] + key[i0%lenkey]) % lenPbox
		tmp=Pbox_temp[i0]
		Pbox_temp[i0]= Pbox_temp[j0]
		Pbox_temp[j0]=tmp
	return Pbox_temp

def Pbox_Generation(DK_Hash_Output_Bits,l):
	DK_Hash_Output_Bits_Final=DK_Hash_Output_Bits
	if l*3*5>len(DK_Hash_Output_Bits):
		len_intermediate=l*3*5-len(DK_Hash_Output_Bits)
		for tt in range(0,ceil(len_intermediate/len(DK_Hash_Output_Bits))):
			DK_Hash_Output_Bits_Final=DK_Hash_Output_Bits_Final+DK_Hash_Output_Bits
	DK_Hash_Required_Iter=[]
	DK_Hash_Required_Iter=DK_Hash_Output_Bits_Final[0:3*5*l]
	Pboxes_Vect_l=[]
	for ii in range(0,l):
		DK_Hash_Required_Iter_l=DK_Hash_Required_Iter[3*5*ii:3*5*ii+3*5]
		pk=[]
		for jj in range(0,3):
			DK_Hash_Required_Iter_l_element=DK_Hash_Required_Iter_l[5*jj:5*jj+5]
			pk.append(int(DK_Hash_Required_Iter_l_element,2))
		pk=np.asarray(pk)
		Pboxes_Vect_l.append(rc4keyperm(pk,9))
	return Pboxes_Vect_l
def Inv_Pbox_Generation(Pbox_Vect):
	Inv_Pbox_Vect=[]
	for tt in range(0,len(Pbox_Vect)):
		Inv_Pbox=np.zeros(9,dtype=int)
		Pbox=np.zeros(9,dtype=int)
		Pbox=Pbox_Vect[tt]
		for ii in range(0,len(Pbox)):
			Inv_Pbox[Pbox[ii]]=ii
		Inv_Pbox_Vect.append(Inv_Pbox)
	return Inv_Pbox_Vect
def Matrix_Modulo(A,N):
	for ii in range(0,A.nrows()):
		for jj in range(0,A.ncols()):
			A[ii,jj]=mod(A[ii,jj],N)
	return A
def Secret_Matrix_Generation(DK_Hash_Output_Bits,l,N,N_Vect,Inverse_Element_Ring_Table):
	Len_Inverse_Element_Ring_Bits=ceil(log(len(Inverse_Element_Ring_Table),2))
	DK_Hash_Output_Bits_Final=DK_Hash_Output_Bits
	if l*3*Len_Inverse_Element_Ring_Bits>len(DK_Hash_Output_Bits):
		len_intermediate=l*3*Len_Inverse_Element_Ring_Bits-len(DK_Hash_Output_Bits)
		for tt in range(0,ceil(len_intermediate/len(DK_Hash_Output_Bits))):
			DK_Hash_Output_Bits_Final=DK_Hash_Output_Bits_Final+DK_Hash_Output_Bits
	DK_Hash_Required_Iter=[]
	DK_Hash_Required_Iter=DK_Hash_Output_Bits_Final[0:3*Len_Inverse_Element_Ring_Bits*l]
	Secret_Matrix_l=[]
	Secret_Matrix_Inverse_l=[]
	for ii in range(0,l):
		DK_Hash_Required_Iter_l=DK_Hash_Required_Iter[3*Len_Inverse_Element_Ring_Bits*ii:3*Len_Inverse_Element_Ring_Bits*ii+3*Len_Inverse_Element_Ring_Bits]
		U=matrix(3,3)
		V=matrix(3,3)
		for jj in range(0,3):
			DK_Hash_Required_Iter_l_element=DK_Hash_Required_Iter_l[Len_Inverse_Element_Ring_Bits*jj:Len_Inverse_Element_Ring_Bits*jj+Len_Inverse_Element_Ring_Bits]
			U[jj,jj]=Inverse_Element_Ring_Table[int(DK_Hash_Required_Iter_l_element,2)]
			for kk in range(0,jj):
				U[jj,kk]=N_Vect[mod(int(DK_Hash_Required_Iter_l_element,2)+20,len(N_Vect))]
			
			V[jj,jj]=Inverse_Element_Ring_Table[mod(int(DK_Hash_Required_Iter_l_element,2)+100,len(Inverse_Element_Ring_Table))]
			for kk in range(0,3-jj-1):
	 			V[jj,3-1-kk]=N_Vect[mod(int(DK_Hash_Required_Iter_l_element,2)+50,len(N_Vect))]	
		U=Matrix_Modulo(U,N)
		V=Matrix_Modulo(V,N)
		Secret_Matrix=matrix(3,3)
		Secret_Matrix=Matrix_Modulo(U*V,N)
		U_inverse=Matrix_Modulo(U.inverse(),N)
		V_inverse=Matrix_Modulo(V.inverse(),N)
		Secret_Matrix_Inverse=matrix(3,3)
		Secret_Matrix_Inverse=Matrix_Modulo(V_inverse*U_inverse,N)
		Secret_Matrix_l.append(Secret_Matrix)
		Secret_Matrix_Inverse_l.append(Secret_Matrix_Inverse)
	return Secret_Matrix_l, Secret_Matrix_Inverse_l
def Matrix_Element_Wise_Product(Key,Plain_text,N):
	Cipher_Matrix_Round=matrix(3,3)
	for ii in range(0,3):
		for jj in range(0,3):
			Cipher_Matrix_Round[ii,jj]=mod(Key[ii,jj]*Plain_text[ii,jj],N)
	return Cipher_Matrix_Round
def Cryptographic_Par_Generation(n,l,N,DK,N_Vect,Inverse_Element_Ring_Table):
	####Hash Generation of n rounds using the DK
	Hash_DK_Vect=Hash_DK_Generator(DK,n)
	#####Generating the Add round keys for the (n+1) rounds
	Add_Round_Key_n_1_Rounds=[]
	Add_Round_Key_Inverse_n_1_Rounds=[]
	######Generating for the Add Round key for the first Add Round Key Step (n=0)
	DK_Hash_Output_0=Hash_DK_Vect[0]
	DK_Hash_Output_Bits_0= ''.join(format(ord(i), '08b') for i in DK_Hash_Output_0)	
	Add_Round_Key_Vector_0=Add_Round_Keys_Generation(DK_Hash_Output_Bits_0,l,Inverse_Element_Ring_Table)
	Add_Round_Key_n_1_Rounds.append(Add_Round_Key_Vector_0)
	Add_Round_Key_Inverse_n_1_Rounds.append(Inverse_Add_Round_Key_Generation(Add_Round_Key_Vector_0,N))
	####Pboxes vector for the n rounds
	Pboxes_Vect_n_Rounds=[]
	Pboxes_Inverse_Vect_n_Rounds=[]
	#####Secret matrices for the n rounds
	Secret_Matrix_n_Rounds=[]
	Secret_Matrix_Inverse_n_Rounds=[]
	######Generating the Cryptographic parameters (Pboxes, Inverse for the n rounds
	for tt in range(0,n):
		Hash_Intermediate=Hash_DK_Vect[tt+1]
		Hash_Intermediate_bits=''.join(format(ord(i), '08b') for i in Hash_Intermediate)
		Pboxes_Vect_n_Rounds.append(Pbox_Generation(Hash_Intermediate_bits,l))
		Pboxes_Inverse_Vect_n_Rounds.append(Inv_Pbox_Generation(Pbox_Generation(Hash_Intermediate_bits,l)))
		Output=Secret_Matrix_Generation(Hash_Intermediate_bits,l,N,N_Vect,Inverse_Element_Ring_Table)
		Secret_Matrix_n_Rounds.append(Output[0])
		Secret_Matrix_Inverse_n_Rounds.append(Output[1])
		Add_Round_Key_n_1_Rounds.append(Add_Round_Keys_Generation(Hash_Intermediate_bits,l,Inverse_Element_Ring_Table))	
		Add_Round_Key_Inverse_n_1_Rounds.append(Inverse_Add_Round_Key_Generation(Add_Round_Keys_Generation(Hash_Intermediate_bits,l,Inverse_Element_Ring_Table),N))
	return Add_Round_Key_n_1_Rounds, Add_Round_Key_Inverse_n_1_Rounds, Pboxes_Vect_n_Rounds, Pboxes_Inverse_Vect_n_Rounds, Secret_Matrix_n_Rounds, Secret_Matrix_Inverse_n_Rounds

def Main_Key_Generation(L,n):
	#### L is the plain-text message size
	#### DK is the Dynamic Key
	#### n is the number of rounds
	#### l is the number of message matrices (3 x3)
	#### N is the public modulus
	##### Generating the public modulus
	p=sympy.randprime(800,900)
	q=sympy.randprime(800,900)
	N=p*q
	print("N=", N)
	#####Generating the Z_N Ring elements in order
	N_Vect=[]
	for tt in range(0,N):
		N_Vect.append(tt)
	#####Generating the ring inverse element
	Inverse_Element_Ring_Table=Inverse_Element_Ring(N)
	#####Generating the dynamic key (DK)
	DK=np.random.randint(1,N-1,9)
	####Encryption and Decryption parameters
	l=ceil(L/9)
	print ("l=", l)
	Cryptographic_Output_Par=Cryptographic_Par_Generation(n,l,N,DK,N_Vect,Inverse_Element_Ring_Table)
	Key_Vector_Add_Round_Key=Cryptographic_Output_Par[0]
	print("Key_Vector_Add_Round_Key=", Key_Vector_Add_Round_Key)
	Key_Vector_Inverse_Add_Round_Key=Cryptographic_Output_Par[1]	
	print("Key_Vector_Inverse_Add_Round_Key=", Key_Vector_Inverse_Add_Round_Key)
	Pboxes_Vector=Cryptographic_Output_Par[2]
	print("Pboxes_Vector=", Pboxes_Vector)
	Pboxes_Inverse_Vector=Cryptographic_Output_Par[3]
	print("Pboxes_Inverse_Vector=", Pboxes_Inverse_Vector)
	Secret_Invertibe_Matrix_Vector=Cryptographic_Output_Par[4]
	print("Secret_Invertibe_Matrix_Vector=", Secret_Invertibe_Matrix_Vector)
	Secret_Invertible_Matrix_Inverse_Vector=Cryptographic_Output_Par[5]
	print("Secret_Invertible_Matrix_Inverse_Vector=", Secret_Invertible_Matrix_Inverse_Vector)
