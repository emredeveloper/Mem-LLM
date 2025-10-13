#!/usr/bin/env python3
"""
Main Script to Run All Mem-Agent Tests
====================================

This script runs all test files and reports results.

Usage:
    python run_all_tests.py          # Run all tests
    python run_all_tests.py basic    # Sadece temel testleri çalıştır
    python run_all_tests.py integration  # Sadece entegrasyon testleri çalıştır
"""

# Test runner - no sys.path manipulation needed after package install

import sys
import unittest
import time
from pathlib import Path


def run_basic_tests():
    """Temel testleri çalıştır"""
    print("🔧 TEMEL TESTLER")
    print("=" * 60)

    # Test modüllerini import et
    from tests import test_mem_agent, test_memory_manager, test_llm_client, test_memory_tools

    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Tüm test modüllerini ekle
    for module in [test_mem_agent, test_memory_manager, test_llm_client, test_memory_tools]:
        suite.addTests(loader.loadTestsFromModule(module))

    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_integration_tests():
    """Entegrasyon testleri çalıştır"""
    print("\n🔗 ENTEGRASYON TESTLERİ")
    print("=" * 60)

    from tests import test_integration
    return test_integration.run_integration_tests()


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

    all_success = True

    if test_type in ["all", "basic"]:
        basic_success = run_basic_tests()
        all_success = all_success and basic_success

    if test_type in ["all", "integration"]:
        integration_success = run_integration_tests()
        all_success = all_success and integration_success

    # Sonuçları göster
    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 70)
    print("📊 TEST SONUÇLARI ÖZETİ")
    print("=" * 70)

    print(f"Toplam süre: {duration:.2f} saniye")

    if all_success:
        print("🎉 TÜM TESTLER BAŞARILI!")
        print("✅ Sistem düzgün çalışıyor!")
    else:
        print("⚠️  BAZI TESTLER BAŞARISIZ!")
        print("🔧 Sorunları çözmeniz gerekebilir.")

    print("=" * 70)

    return all_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

