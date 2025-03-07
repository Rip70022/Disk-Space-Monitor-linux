import psutil
import time
import os
import json
import platform
import logging
from pathlib import Path
import ctypes
import shutil
from datetime import datetime

def load_language(lang='en'):
    languages = {
        'en': {
            'disk_alert_title': 'Disk Space Alert',
            'disk_alert_message': 'Low disk space detected on {}\nUsage: {}%\nThreshold: {}%',
            'monitoring': 'Monitoring disk usage...',
            'config_error': 'Configuration error:',
            'path_not_found': 'Path not found:',
            'log_started': 'Disk monitoring started',
            'log_alert': 'Disk space alert triggered',
            'backup_started': 'Starting backup process',
            'backup_completed': 'Backup completed',
            'backup_failed': 'Backup failed'
        },
        'es': {
            'disk_alert_title': 'Alerta de Espacio en Disco',
            'disk_alert_message': 'Espacio bajo en disco detectado en {}\nUso: {}%\nUmbral: {}%',
            'monitoring': 'Monitoreando uso del disco...',
            'config_error': 'Error de configuración:',
            'path_not_found': 'Ruta no encontrada:',
            'log_started': 'Monitoreo de disco iniciado',
            'log_alert': 'Alerta de espacio en disco activada',
            'backup_started': 'Iniciando proceso de respaldo',
            'backup_completed': 'Respaldo completado',
            'backup_failed': 'Error en el respaldo'
        },
        'fr': {
            'disk_alert_title': 'Alerte d\'Espace Disque',
            'disk_alert_message': 'Espace disque faible détecté sur {}\nUtilisation: {}%\nSeuil: {}%',
            'monitoring': 'Surveillance de l\'utilisation du disque...',
            'config_error': 'Erreur de configuration:',
            'path_not_found': 'Chemin non trouvé:',
            'log_started': 'Surveillance du disque démarrée',
            'log_alert': 'Alerte d\'espace disque déclenchée',
            'backup_started': 'Démarrage du processus de sauvegarde',
            'backup_completed': 'Sauvegarde terminée',
            'backup_failed': 'Échec de la sauvegarde'
        },
        'de': {
            'disk_alert_title': 'Festplattenplatz-Warnung',
            'disk_alert_message': 'Niedriger Festplattenplatz erkannt auf {}\nNutzung: {}%\nSchwelle: {}%',
            'monitoring': 'Überwachung der Festplattennutzung...',
            'config_error': 'Konfigurationsfehler:',
            'path_not_found': 'Pfad nicht gefunden:',
            'log_started': 'Festplattenüberwachung gestartet',
            'log_alert': 'Festplattenplatz-Warnung ausgelöst',
            'backup_started': 'Backup-Prozess wird gestartet',
            'backup_completed': 'Backup abgeschlossen',
            'backup_failed': 'Backup fehlgeschlagen'
        },
        'it': {
            'disk_alert_title': 'Avviso Spazio Disco',
            'disk_alert_message': 'Rilevato spazio disco insufficiente su {}\nUtilizzo: {}%\nSoglia: {}%',
            'monitoring': 'Monitoraggio dell\'uso del disco...',
            'config_error': 'Errore di configurazione:',
            'path_not_found': 'Percorso non trovato:',
            'log_started': 'Monitoraggio del disco avviato',
            'log_alert': 'Avviso di spazio su disco attivato',
            'backup_started': 'Avvio del processo di backup',
            'backup_completed': 'Backup completato',
            'backup_failed': 'Backup fallito'
        },
        'pt': {
            'disk_alert_title': 'Alerta de Espaço em Disco',
            'disk_alert_message': 'Pouco espaço em disco detectado em {}\nUso: {}%\nLimite: {}%',
            'monitoring': 'Monitorando uso do disco...',
            'config_error': 'Erro de configuração:',
            'path_not_found': 'Caminho não encontrado:',
            'log_started': 'Monitoramento de disco iniciado',
            'log_alert': 'Alerta de espaço em disco acionado',
            'backup_started': 'Iniciando processo de backup',
            'backup_completed': 'Backup concluído',
            'backup_failed': 'Falha no backup'
        },
        'ru': {
            'disk_alert_title': 'Предупреждение о дисковом пространстве',
            'disk_alert_message': 'Обнаружено мало места на диске {}\nИспользование: {}%\nПорог: {}%',
            'monitoring': 'Мониторинг использования диска...',
            'config_error': 'Ошибка конфигурации:',
            'path_not_found': 'Путь не найден:',
            'log_started': 'Мониторинг диска запущен',
            'log_alert': 'Сработало предупреждение о дисковом пространстве',
            'backup_started': 'Запуск процесса резервного копирования',
            'backup_completed': 'Резервное копирование завершено',
            'backup_failed': 'Ошибка резервного копирования'
        },
        'ja': {
            'disk_alert_title': 'ディスク容量警告',
            'disk_alert_message': '{}でディスク容量不足が検出されました\n使用率: {}%\nしきい値: {}%',
            'monitoring': 'ディスク使用状況を監視中...',
            'config_error': '設定エラー:',
            'path_not_found': 'パスが見つかりません:',
            'log_started': 'ディスク監視を開始しました',
            'log_alert': 'ディスク容量警告がトリガーされました',
            'backup_started': 'バックアッププロセスを開始します',
            'backup_completed': 'バックアップが完了しました',
            'backup_failed': 'バックアップに失敗しました'
        },
        'zh': {
            'disk_alert_title': '磁盘空间警告',
            'disk_alert_message': '在{}上检测到磁盘空间不足\n使用率: {}%\n阈值: {}%',
            'monitoring': '监控磁盘使用情况...',
            'config_error': '配置错误:',
            'path_not_found': '找不到路径:',
            'log_started': '磁盘监控已开始',
            'log_alert': '磁盘空间警告已触发',
            'backup_started': '开始备份过程',
            'backup_completed': '备份完成',
            'backup_failed': '备份失败'
        }
    }
    
    return languages.get(lang, languages['en'])

class DiskMonitor:
    def __init__(self, config_path='config.json'):
        self.config = self.load_config(config_path)
        self.lang = load_language(self.config.get('language', 'en'))
        self.setup_logging()
        self.logger.info(self.lang['log_started'])
        self.show_ascii_banner()
    
    def load_config(self, config_path):
        default_config = {
            'language': 'en',
            'disk_paths': ['C:\\'],
            'threshold_percent': 90,
            'check_interval': 300,
            'alert_color': {
                'background': 'red',
                'text': 'white'
            },
            'backup': {
                'enabled': False,
                'source_dirs': [],
                'destination_dir': '',
                'max_backups': 5
            },
            'log_file': 'disk_monitor.log'
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return {**default_config, **json.load(f)}
            else:
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            print(f"{load_language()['config_error']} {e}")
            return default_config
    
    def setup_logging(self):
        self.logger = logging.getLogger('DiskMonitor')
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(self.config['log_file'])
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
    
    def show_ascii_banner(self):
        banner = """
    ____  _      __    __  __            _ __            
   / __ \(_)____/ /___/ /_/ /_____  ____(_) /_____  _____
  / / / / / ___/ //_/ __/ __/ __ \/ ___/ / __/ __ \/ ___/
 / /_/ / (__  ) ,< / /_/ /_/ /_/ / /  / / /_/ /_/ / /    
/_____/_/____/_/|_|\__/\__/\____/_/  /_/\__/\____/_/     
                                                         
        Disk Space Monitor / diskttoritor v1.0
        Created by: https://www.github.com/Rip70022
        """
        print(banner)
    
    def check_disk_usage(self, path):
        try:
            usage = psutil.disk_usage(path)
            return usage.percent
        except FileNotFoundError:
            print(f"{self.lang['path_not_found']} {path}")
            self.logger.error(f"{self.lang['path_not_found']} {path}")
            return None
    
    def show_windows_alert(self, title, message, style=0):
        color_map = {
            'red': 0x0000000C,
            'blue': 0x00000001,
            'green': 0x00000002,
            'yellow': 0x00000006,
            'purple': 0x00000005,
            'white': 0x00000007
        }
        
        bg_color = color_map.get(self.config['alert_color']['background'].lower(), 0x0000000C)
        
        if platform.system() == 'Windows':
            ctypes.windll.user32.MessageBoxW(0, message, title, style | bg_color)
        else:
            color_codes = {
                'red': '\033[41m',
                'blue': '\033[44m',
                'green': '\033[42m',
                'yellow': '\033[43m',
                'purple': '\033[45m',
                'white': '\033[47m',
                'black': '\033[40m'
            }
            
            text_color_codes = {
                'red': '\033[31m',
                'blue': '\033[34m',
                'green': '\033[32m',
                'yellow': '\033[33m',
                'purple': '\033[35m',
                'white': '\033[37m',
                'black': '\033[30m'
            }
            
            bg_color_code = color_codes.get(self.config['alert_color']['background'].lower(), '\033[41m')
            text_color_code = text_color_codes.get(self.config['alert_color']['text'].lower(), '\033[37m')
            reset = '\033[0m'
            
            print("\n" + "="*50)
            print(f"{bg_color_code}{text_color_code}{title.center(48)}{reset}")
            print("="*50)
            for line in message.split('\n'):
                print(f"{text_color_code}{line}{reset}")
            print("="*50 + "\n")
    
    def perform_backup(self):
        if not self.config['backup']['enabled'] or not self.config['backup']['source_dirs'] or not self.config['backup']['destination_dir']:
            return
        
        self.logger.info(self.lang['backup_started'])
        
        try:
            backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(self.config['backup']['destination_dir'], f"backup_{backup_time}")
            
            os.makedirs(backup_dir, exist_ok=True)
            
            for source_dir in self.config['backup']['source_dirs']:
                if os.path.exists(source_dir):
                    dest_path = os.path.join(backup_dir, os.path.basename(source_dir))
                    shutil.copytree(source_dir, dest_path)
            
            backups = sorted([d for d in os.listdir(self.config['backup']['destination_dir']) if d.startswith("backup_")])
            
            if len(backups) > self.config['backup']['max_backups']:
                for old_backup in backups[:len(backups) - self.config['backup']['max_backups']]:
                    old_path = os.path.join(self.config['backup']['destination_dir'], old_backup)
                    shutil.rmtree(old_path)
            
            self.logger.info(self.lang['backup_completed'])
        except Exception as e:
            self.logger.error(f"{self.lang['backup_failed']}: {e}")
    
    def alert(self, path, usage):
        self.logger.warning(self.lang['log_alert'])
        
        title = self.lang['disk_alert_title']
        message = self.lang['disk_alert_message'].format(path, usage, self.config['threshold_percent'])
        
        self.show_windows_alert(title, message)
        
        if self.config['backup']['enabled']:
            self.perform_backup()
    
    def start_monitoring(self):
        print(self.lang['monitoring'])
        
        while True:
            for path in self.config['disk_paths']:
                usage = self.check_disk_usage(path)
                
                if usage is not None and usage > self.config['threshold_percent']:
                    self.alert(path, usage)
            
            time.sleep(self.config['check_interval'])

if __name__ == "__main__":
    monitor = DiskMonitor()
    monitor.start_monitoring()
