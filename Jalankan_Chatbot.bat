@echo off
title Mesin Server Chatbot Dokumen AI
cd /d "%~dp0"
cls
echo ======================================================================
echo           MESIN SERVER CHATBOT DOKUMEN AI SEDANG AKTIF
echo ======================================================================
echo.
echo [PENTING] JANGAN TUTUP JENDELA HITAM INI!
echo Jendela ini adalah "mesin" yang memproses pertanyaan Anda di website.
echo Anda boleh MEMINIMALKAN (minimize) jendela ini ke taskbar.
echo.
echo Sedang membuka browser otomatis ke alamat: http://127.0.0.1:5000 ...
echo ======================================================================
echo.
python app.py
echo.
echo Server telah berhenti.
pause
