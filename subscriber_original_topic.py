import paho.mqtt.client as mqtt
import json
import time

broker_address = "test.mosquitto.org"
port = 1883
topic = "Universitas Teknologi Yogyakarta/Fajri Maulana Yusuf"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[OK] Subscriber berhasil terhubung ke Broker!")
        client.subscribe(topic)
        print(f"[INFO] Berlangganan ke topik ASLI: '{topic}'")
    else:
        print(f"Gagal terhubung, kode balasan: {rc}")

def on_disconnect(client, userdata, flags, rc, properties=None):
    if rc != 0:
        print("[WARNING] Koneksi terputus secara tidak terduga")

def on_message(client, userdata, msg):
    try:
        message_string = msg.payload.decode('utf-8')
        
        message_data = json.loads(message_string)
        
        print(f"\n[MESSAGE] Pesan diterima dari topik: {msg.topic}")
        print(f"   Pesan ke: {message_data.get('pesan_ke', 'N/A')}")
        print(f"   Isi: {message_data.get('isi', 'N/A')}")
        print(f"   Pengirim: {message_data.get('sender', 'N/A')}")
        print(f"   Universitas: {message_data.get('universitas', 'N/A')}")
        print(f"   NIM: {message_data.get('nim', 'N/A')}")
        print(f"   Topik Asli: {message_data.get('topik_asli', 'N/A')}")
        print(f"   Timestamp: {time.ctime(message_data.get('timestamp', 0))}")
        print("-" * 60)
        
    except json.JSONDecodeError:
        print(f"[MESSAGE] Pesan diterima (bukan JSON): {msg.payload.decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] Error saat memproses pesan: {e}")

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2, 
    client_id="Subscriber_Client_Fajri_Original_Topic", 
    protocol=mqtt.MQTTv311
)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print(f"Menghubungkan subscriber ke broker di {broker_address}...")
print(f"[INFO] Akan berlangganan ke topik ASLI: '{topic}'")

try:
    client.connect(broker_address, port, 60)
    
    print("[INFO] Menunggu pesan... (Tekan Ctrl+C untuk keluar)")
    
    client.loop_forever()
    
except KeyboardInterrupt:
    print("\n[INFO] Program dihentikan oleh user")
except Exception as e:
    print(f"[ERROR] Error: {e}")
finally:
    client.disconnect()
    print("[INFO] Koneksi subscriber ditutup.")