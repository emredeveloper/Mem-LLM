#!/usr/bin/env python3
"""
Tüm Mem-Agent Testlerini Çalıştıran Ana Script
===========================================

Bu script tüm test dosyalarını çalıştırır ve sonuçları raporlar.

Kullanım:
    python run_all_tests.py          # Tüm testleri çalıştır
    python run_all_tests.py basic    # Sadece temel testleri çalıştır
    python run_all_tests.py pro      # Sadece Pro testleri çalıştır
    python run_all_tests.py integration  # Sadece entegrasyon testleri çalıştır
"""

import sys
import unittest
import time
from pathlib import Path


def run_test_file(test_file, description):
    """Belirli bir test dosyasını çalıştırır"""
    print(f"\n🧪 {description}")
    print("=" * 60)

    try:
        # Test modülünü import et ve çalıştır
        module_name = test_file.replace('.py', '')
        exec(f"import {module_name}")

        # Test çalıştırma fonksiyonunu çağır
        exec(f"success = {module_name}.run_specific_test('all') if hasattr({module_name}, 'run_specific_test') else True")

        if 'success' in locals() and success:
            print(f"✅ {description} - BAŞARILI")
            return True
        else:
            print(f"❌ {description} - BAŞARISIZ")
            return False

    except Exception as e:
        print(f"❌ {description} - HATA: {e}")
        return False


def run_basic_tests():
    """Temel testleri çalıştır"""
    print("🔧 TEMEL TESTLER")
    print("=" * 60)

    success_count = 0
    total_count = 0

    # Temel test dosyaları
    basic_tests = [
        ("test_mem_agent", "MemAgent Temel Testleri"),
        ("test_memory_manager", "MemoryManager Testleri"),
        ("test_llm_client", "LLM Client Testleri"),
        ("test_memory_tools", "Araçlar Sistemi Testleri")
    ]

    for test_file, description in basic_tests:
        total_count += 1
        if run_test_file(test_file, description):
            success_count += 1

    return success_count, total_count


def run_pro_tests():
    """Pro testleri çalıştır"""
    print("\n🚀 PRO TESTLER")
    print("=" * 60)

    try:
        import test_mem_agent_pro
        success = test_mem_agent_pro.run_pro_tests()
        return 1 if success else 0, 1
    except ImportError:
        print("⚠️  Pro testleri çalıştırılamadı (modüller eksik)")
        return 0, 1


def run_integration_tests():
    """Entegrasyon testleri çalıştır"""
    print("\n🔗 ENTEGRASYON TESTLERİ")
    print("=" * 60)

    try:
        import test_integration
        success = test_integration.run_integration_tests()
        return 1 if success else 0, 1
    except ImportError:
        print("⚠️  Entegrasyon testleri çalıştırılamadı")
        return 0, 1


def main():
    """Ana test çalıştırma fonksiyonu"""
    print("🧪 MEM-AGENT KAPSAMLI TEST SUITE")
    print("=" * 70)
    print(f"Başlangıç zamanı: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    start_time = time.time()

    # Hangi testleri çalıştıracağımızı belirle
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        test_type = "all"

    success_count = 0
    total_count = 0

    if test_type in ["all", "basic"]:
        basic_success, basic_total = run_basic_tests()
        success_count += basic_success
        total_count += basic_total

    if test_type in ["all", "pro"]:
        pro_success, pro_total = run_pro_tests()
        success_count += pro_success
        total_count += pro_total

    if test_type in ["all", "integration"]:
        integration_success, integration_total = run_integration_tests()
        success_count += integration_success
        total_count += integration_total

    # Sonuçları göster
    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 70)
    print("📊 TEST SONUÇLARI ÖZETİ")
    print("=" * 70)

    print(f"Toplam süre: {duration:.2f} saniye")
    print(f"Başarılı testler: {success_count}/{total_count}")

    if success_count == total_count:
        print("🎉 TÜM TESTLER BAŞARILI!")
        print("✅ Sistem düzgün çalışıyor!")
    else:
        print("⚠️  BAZI TESTLER BAŞARISIZ!")
        print("🔧 Sorunları çözmeniz gerekebilir.")

    print("=" * 70)

    # Detaylı başarı oranı
    if total_count > 0:
        success_rate = (success_count / total_count) * 100
        print(f"Başarı oranı: {success_rate:.1f}%")

    return success_count == total_count


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
