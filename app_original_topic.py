import paho.mqtt.client as mqtt
import json
import time
import socket

broker_address = "test.mosquitto.org"
port = 1883
topic = "Universitas Teknologi Yogyakarta/Fajri Maulana Yusuf"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[OK] Berhasil terhubung ke Broker!")
    else:
        print(f"[ERROR] Gagal terhubung, kode balasan: {rc}")

def on_disconnect(client, userdata, flags, rc, properties=None):
    if rc != 0:
        print("[WARNING] Koneksi terputus secara tidak terduga")

def on_publish(client, userdata, mid, reason_code=None, properties=None):
    print(f"   -> Pesan dengan ID {mid} berhasil dipublish")

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="Publisher_Client_Fajri_Original_Topic",
    protocol=mqtt.MQTTv311
)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

print(f"Menghubungkan ke broker di {broker_address}...")
print(f"[INFO] Menggunakan topik ASLI sesuai tugas: '{topic}'")

try:
    client.connect(broker_address, port, 60)
    
    client.loop_start()
    time.sleep(2)
    
    if client.is_connected():
        print(f"[INFO] Mulai mengirim 5 pesan ke topik: '{topic}'")
        
        for i in range(1, 6):
            payload = {
                "pesan_ke": i,
                "isi": f"Ini adalah pesan nomor {i} dari Fajri Maulana Yusuf",
                "timestamp": time.time(),
                "sender": "Fajri Maulana Yusuf",
                "universitas": "Universitas Teknologi Yogyakarta",
                "nim": "5241011005",
                "topik_asli": "Universitas Teknologi Yogyakarta/Fajri Maulana Yusuf"
            }
            
            json_payload = json.dumps(payload, ensure_ascii=False)
            
            result = client.publish(topic, json_payload, qos=0)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"   -> Pesan ke-{i} berhasil dikirim.")
            else:
                print(f"   -> [ERROR] Gagal mengirim pesan ke-{i}")
            
            time.sleep(1)
        
        time.sleep(2)
        
    else:
        print("[ERROR] Tidak dapat terhubung ke broker")

except socket.timeout:
    print("[ERROR] Koneksi timeout. Periksa koneksi internet atau coba broker lain.")
except ConnectionRefusedError:
    print("[ERROR] Koneksi ditolak. Broker mungkin tidak tersedia.")
except Exception as e:
    print(f"[ERROR] Error: {e}")

finally:
    client.loop_stop()
    client.disconnect()
    print("[INFO] Koneksi ditutup. Program selesai.")