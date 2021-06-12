#include "inter.h"
#include <stdio.h>
using namespace System;
#using "C:\Users\markb\source\repos\PySec\PythonCSharp\bin\Release\net5.0\PythonCSharp.dll"  //Asssembly
using namespace intdotnet;
#include <string.h>
using namespace System::Runtime::InteropServices;
#include < stdlib.h >
#include < vcclr.h >
#include<tuple>
#include <iostream> 
using namespace std;
#pragma unmanaged
static class pythonconnect{
	static std::tuple<char[], char[]> AesEncrypt(char text[], char key[]){
		return crypto::AESEncrypt(text, key);
	}
	static char* AesDecrypt(char iv[], char key[], char ctext[]) {
		return crypto::AESDecrypt(iv, key, ctext);
	}
};
#pragma managed
static class crypto {
	public:
		static std::tuple<char, char> AESEncrypt(char text[], char key[]) {
			cli::array< Byte >^ bytekey = gcnew cli::array< Byte > (strlen(key));
			Marshal::Copy((IntPtr)key, bytekey, 0, strlen(key));
			GCHandle handlekey = GCHandle::Alloc(bytekey, GCHandleType::Pinned);
			for (int i = 0; i < strlen(key); i++) {
				char* ptr = &key[i];
				*ptr = 0;
			}


			cli::array< Byte >^ bytetext = gcnew cli::array< Byte > (strlen(text));
			Marshal::Copy((IntPtr)text, bytetext, 0, strlen(key));
			GCHandle handleiv = GCHandle::Alloc(bytetext, GCHandleType::Pinned);
			for (int i = 0; i < strlen(text); i++) {
				char* ptr = &text[i];
				*ptr = 0;
			}

			ValueTuple<cli::array <unsigned char>^, cli::array <unsigned char>^>  result = Crypto::AESEncrypt(bytetext, bytekey);
			GCHandle handleresult = GCHandle::Alloc(result, GCHandleType::Pinned);
			char* iv = new char[(result.Item1->Length) + 1];
			char* ctext = new char[(result.Item2->Length)];


			for (int i = 0; i < result.Item1->Length; i++) {
				ctext[i] = result.Item1[i];
			}
			for (int i = 0; i < result.Item2->Length; i++) {
				ctext[i] = result.Item2[i];
			}
			for (int i = 0; i < bytekey->Length; i++) {
				auto pbArr2 = &bytekey[i];
				*pbArr2 = 0;
			}
			for (int i = 0; i < bytetext->Length; i++) {
				auto pbArr2 = &bytetext[i];
				*pbArr2 = 0;
			}
			delete bytekey;
			delete bytetext;
			delete text;
			delete key;
			delete result;
			return {*ctext, *iv};
		}

		static char* AESDecrypt(char iv[], char key[], char ctext[]) {
			cli::array< Byte >^ bytekey = gcnew cli::array< Byte > (strlen(key));
			Marshal::Copy((IntPtr)key, bytekey, 0, strlen(key));
			GCHandle handlekey = GCHandle::Alloc(bytekey, GCHandleType::Pinned);
			for (int i = 0; i < strlen(key); i++) {
				char* ptr = &key[i];
				*ptr = 0;
			}

			cli::array< Byte >^ byteiv = gcnew cli::array< Byte > (strlen(iv));
			Marshal::Copy((IntPtr)iv, byteiv, 0, strlen(key));
			GCHandle handleiv = GCHandle::Alloc(byteiv, GCHandleType::Pinned);

			cli::array< Byte >^ bytectext = gcnew cli::array< Byte > (strlen(ctext));
			Marshal::Copy((IntPtr)ctext, bytectext, 0, strlen(ctext));
			GCHandle handlectext = GCHandle::Alloc(bytectext, GCHandleType::Pinned);

			String^ result = Crypto::AESDecrypt(bytekey, bytectext, byteiv);
			GCHandle handleresult = GCHandle::Alloc(result, GCHandleType::Pinned);

			char* r = new char[(result->Length) + 1];

			for (int i = 0; i < result->Length; i++) {
				r[i] = result[i];
				auto* n = &result; // Reset it to avoid memory leaks -- still needs finsihing
				*n = " ";
			}

			for (int i = 0; i < bytekey->Length; i++) {
				auto pbArr2 = &bytekey[i];
				*pbArr2 = 0;
			}

			Array::Clear(bytekey, 0, bytekey->Length);
			Array::Clear(byteiv, 0, byteiv->Length);
			Array::Clear(bytectext, 0, bytectext->Length);
			handlekey.Free();
			delete bytekey;
			delete byteiv;
			delete bytectext;
			delete handelkey;
			delete result;
			delete handelresult;
			delete iv;
			delete key;
			delete ctext;
			return r;
		}

};