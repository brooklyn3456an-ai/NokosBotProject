import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- 1. DATA BOT (SUDAH DIKUSTOMISASI) ---
ID_ADMIN = 5278941890 
REKENING = "SHOPEEPAY ATAU DANA - 085865121145"
TRANSAKSI_PENDING = {} 

PRODUCTS = {
    # NOKOS
    'AKULAKU': {'harga': 1700, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'BLIBLI': {'harga': 1400, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'CGV': {'harga': 1400, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'DANA': {'harga': 1400, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'FORECOFFEE': {'harga': 1000, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'GOJEK': {'harga': 1400, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'GRAB': {'harga': 1000, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'KOPIKENANGAN': {'harga': 2000, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'LAZADA': {'harga': 1400, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'MICROSOFT': {'harga': 1000, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'NETFLIX_NOKOS': {'harga': 1400, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'QPON': {'harga': 1400, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'SHOPEE_NOKOS': {'harga': 1400, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'STARBUCK': {'harga': 1400, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'TELEGRAM': {'harga': 9500, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'TIKTOK': {'harga': 1300, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'TOKOPEDIA': {'harga': 1300, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    'WHATSAPP': {'harga': 7500, 'jenis': 'NOKOS', 'note': 'NON GARANSI'},
    
    # PREMIUM APPS (FLAGGED AS PO)
    'PO_ALIGHTMOTION_365D': {'harga': 10000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_CANVA_OWNER_30D': {'harga': 10500, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_CANVA_INVITE_30D': {'harga': 5000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_CAPCUT_21D': {'harga': 9000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_CHATGPT_30D': {'harga': 28500, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_IQIYI_300D': {'harga': 13000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_NETFLIX_30D': {'harga': 33000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_OFFICE_365D': {'harga': 38000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_VIDIOPLATINUM_30D': {'harga': 28000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_VIU_365D': {'harga': 38000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_WETV_30D_PRIVATE': {'harga': 33000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_WETV_30D_SHARING': {'harga': 13000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_WETV_60D_SHARING': {'harga': 18000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
    'PO_ZOOM_14D': {'harga': 1000, 'jenis': 'PREMIUM', 'note': 'PO (5 MENIT - 3 JAM)'},
}

# --- 2. HANDLER PERINTAH & MENU ---

# Helper function to format product name for display
def format_product_name(key):
    return key.replace('PO_', '').replace('_', ' ').title().replace('365D', '(365 HARI)').replace('30D', '(30 HARI)').replace('60D', '(60 HARI)').replace('14D', '(14 HARI)').replace('1P 1U', '1 PROFIL 1 USER').replace('Nokos', 'NOKOS')

# Perintah: /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("✅ NOKOS", callback_data='menu_NOKOS')],
        [InlineKeyboardButton("⭐ APLIKASI PREMIUM (PO)", callback_data='menu_PREMIUM')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("SELAMAT DATANG DI BOT KAMI! SILAKAN PILIH KATEGORI PRODUK:", reply_markup=reply_markup)
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("SELAMAT DATANG DI BOT KAMI! SILAKAN PILIH KATEGORI PRODUK:", reply_markup=reply_markup)


# Menu NOKOS
async def menu_nokos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    nokos_products = [key for key, val in PRODUCTS.items() if val['jenis'] == 'NOKOS']
    
    # Buat tombol 2 kolom
    for i in range(0, len(nokos_products), 2):
        row = []
        key1 = nokos_products[i]
        row.append(InlineKeyboardButton(f"{format_product_name(key1)} (RP {PRODUCTS[key1]['harga']:,.0f})", callback_data=f'beli_{key1}'))
        
        if i + 1 < len(nokos_products):
            key2 = nokos_products[i+1]
            row.append(InlineKeyboardButton(f"{format_product_name(key2)} (RP {PRODUCTS[key2]['harga']:,.0f})", callback_data=f'beli_{key2}'))
        
        keyboard.append(row)
        
    keyboard.append([InlineKeyboardButton("⬅️ KEMBALI KE MENU UTAMA", callback_data='start_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "PILIH NOKOS YANG ANDA INGINKAN (HARGA NON GARANSI):",
        reply_markup=reply_markup
    )

# Menu PREMIUM
async def menu_premium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    premium_products = [key for key, val in PRODUCTS.items() if val['jenis'] == 'PREMIUM']
    
    for key in premium_products:
        harga = PRODUCTS[key]['harga']
        nama = format_product_name(key)
        keyboard.append([InlineKeyboardButton(f"⭐ {nama} (RP {harga:,.0f})", callback_data=f'beli_{key}')])

    keyboard.append([InlineKeyboardButton("⬅️ KEMBALI KE MENU UTAMA", callback_data='start_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "PILIH APLIKASI PREMIUM (PROSES PO 5 MENIT - 3 JAM SAAT ADMIN ONLINE):",
        reply_markup=reply_markup
    )

# Perintah Beli (Dipicu oleh tombol inline)
async def beli_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    product_key = query.data.split('_')[1]
    product_data = PRODUCTS.get(product_key)
    
    if not product_data:
        await query.edit_message_text("PRODUK TIDAK DITEMUKAN.")
        return

    if user_id in TRANSAKSI_PENDING:
        del TRANSAKSI_PENDING[user_id]
        
    kode_unik = random.randint(100, 999)
    harga_dasar = product_data['harga']
    total_bayar = harga_dasar + kode_unik
    
    TRANSAKSI_PENDING[user_id] = {'jumlah': total_bayar, 'produk': product_key}
    
    instruksi = (
        f"**[FAKTUR PEMBELIAN: {format_product_name(product_key)}]**\n"
        f"Harga Produk: RP {harga_dasar:,.0f}\n"
        f"Kode Unik (WAJIB): RP {kode_unik}\n"
        f"-----------------------------------------\n"
        f"**TOTAL BAYAR: RP {total_bayar:,.0f}**\n\n"
        
        f"**REKENING TUJUAN:** {REKENING}\n\n"
        f"**NOTE:** {product_data['note']}\n\n"
        f"**PERHATIAN:** KHUSUS NOKOS, VERIFIKASI HANYA DILAYANI VIA SMS! SELAIN SMS TIDAK BISA DILAYANI.\n\n"
        
        "**LANGKAH SELANJUTNYA:**\n"
        "1. TRANSFER TEPAT sebesar RP " + f"{total_bayar:,.0f}" + ".\n"
        f"2. Setelah transfer, kirim perintah ini untuk konfirmasi:\n"
        f"`/konfirmasi {total_bayar}`"
    )
    
    await query.edit_message_text(instruksi, parse_mode='Markdown')

# Perintah: /konfirmasi [jumlah]
async def konfirmasi_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    
    if len(context.args) != 1:
        await update.message.reply_text("FORMAT SALAH. GUNAKAN: `/KONFIRMASI [TOTAL JUMLAH YANG DITRANSFER]`")
        return

    try:
        jumlah_konfirmasi = int(context.args[0].replace('.', '').replace(',', ''))
    except ValueError:
        await update.message.reply_text("JUMLAH HARUS BERUPA ANGKA.")
        return
    
    transaksi = TRANSAKSI_PENDING.get(user_id)
    
    if not transaksi or transaksi['jumlah'] != jumlah_konfirmasi:
        await update.message.reply_text("TRANSAKSI TIDAK DITEMUKAN ATAU JUMLAH TRANSFER TIDAK SESUAI.")
        return
    
    await update.message.reply_text(
        f"KONFIRMASI PEMBAYARAN SEBESAR RP {jumlah_konfirmasi:,.0f} DITERIMA.\n"
        "**MOHON TUNGGU** SELAGI ADMIN MEMVERIFIKASI MUTASI BANK ANDA SECARA MANUAL."
    )
    
    # Notifikasi ke Admin
    await context.bot.send_message(
        chat_id=ID_ADMIN,
        text=f"🚨 **BUTUH VERIFIKASI ADMIN!**\n\nPRODUK: {format_product_name(transaksi['produk'])}\nUSER ID: {user_id}\nJUMLAH KONFIRMASI: RP {jumlah_konfirmasi:,.0f}\n\nKetik: `/deliver {user_id} {transaksi['produk']}` setelah OK."
    )
    

# Perintah Admin: /deliver [USER_ID] [PRODUCT_KEY]
async def deliver_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id != ID_ADMIN: 
        await update.message.reply_text("ANDA TIDAK MEMILIKI IZIN ADMIN.")
        return
    
    if len(context.args) != 2:
        await update.message.reply_text("FORMAT SALAH. GUNAKAN: /DELIVER [USER_ID_PEMBELI] [PRODUCT_KEY]")
        return
        
    try:
        pembeli_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID Pembeli harus berupa angka.")
        return
        
    product_key = context.args[1]
    
    if pembeli_id in TRANSAKSI_PENDING:
        del TRANSAKSI_PENDING[pembeli_id]

    # Mengirim notifikasi pengiriman ke pembeli
    await context.bot.send_message(
        chat_id=pembeli_id,
        text=f"✅ **PEMBAYARAN DIVERIFIKASI!**\n\nPRODUK: **{format_product_name(product_key)}** sedang diproses (sesuai note yang tertera).\n\nSILAKAN TUNGGU INSTRUKSI LEBIH LANJUT DARI ADMIN UNTUK PENGIRIMAN NOKOS/AKUN. **PERHATIAN: VERIFIKASI HANYA DILAYANI VIA SMS!** TERIMA KASIH TELAH BERBELANJA!",
        parse_mode='Markdown'
    )
    
    await update.message.reply_text(f"PENGIRIMAN PRODUK {format_product_name(product_key)} KE ID {pembeli_id} TELAH DIBERIKAN NOTIFIKASI SUKSES.")


# --- 3. FUNGSI UTAMA BOT ---
def main():
    TOKEN = os.environ.get("BOT_TOKEN") 
    
    if not TOKEN:
        print("ERROR: VARIABEL LINGKUNGAN BOT_TOKEN TIDAK DITEMUKAN.")
        return

    application = Application.builder().token(TOKEN).build()

    # Handlers untuk perintah
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("konfirmasi", konfirmasi_command))
    application.add_handler(CommandHandler("deliver", deliver_command))
    
    # Handlers untuk tombol inline (CallbackQueryHandler)
    application.add_handler(CallbackQueryHandler(start_command, pattern='^start_menu$'))
    application.add_handler(CallbackQueryHandler(menu_nokos, pattern='^menu_NOKOS$'))
    application.add_handler(CallbackQueryHandler(menu_premium, pattern='^menu_PREMIUM$'))
    application.add_handler(CallbackQueryHandler(beli_callback, pattern='^beli_'))

    print("BOT BERJALAN DAN MENDENGARKAN...")
    application.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()
