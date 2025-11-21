#!/usr/bin/env python3
"""
Script para verificar e corrigir o banco de dados
"""
import sqlite3

def verificar_banco():
    import os
    
    print("🔍 Verificando banco de dados...")
    
    # Verificar se o arquivo existe
    if not os.path.exists('instance/financas.db'):
        print("❌ Arquivo instance/financas.db não encontrado!")
        print("   Execute: python criar_banco_novo.py")
        return
    
    # Ver tamanho do arquivo
    tamanho = os.path.getsize('instance/financas.db')
    print(f"📁 Arquivo: instance/financas.db ({tamanho} bytes)")
    
    if tamanho == 0:
        print("❌ Arquivo está vazio!")
        return
    
    conn = sqlite3.connect('instance/financas.db')
    cursor = conn.cursor()
    
    # Verificar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [t[0] for t in cursor.fetchall()]
    
    print(f"\n📋 Tabelas encontradas: {len(tabelas)}")
    for t in tabelas:
        print(f"   - {t}")
    
    # Verificar colunas da despesa_fixa
    if 'despesa_fixa' in tabelas:
        print("\n🔍 Colunas da tabela despesa_fixa:")
        cursor.execute("PRAGMA table_info(despesa_fixa)")
        colunas = cursor.fetchall()
        
        colunas_nomes = []
        for col in colunas:
            print(f"   - {col[1]} ({col[2]})")
            colunas_nomes.append(col[1])
        
        # Verificar se faltam colunas
        colunas_necessarias = ['pago_por_user_id', 'data_pagamento']
        faltando = [c for c in colunas_necessarias if c not in colunas_nomes]
        
        if faltando:
            print(f"\n⚠️  Colunas faltando: {faltando}")
            print("   Execute: python atualizar_sistema.py")
        else:
            print("\n✅ Todas as colunas necessárias estão presentes!")
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM despesa_fixa")
        total = cursor.fetchone()[0]
        print(f"\n📊 Total de despesas fixas: {total}")
        
        if total > 0:
            cursor.execute("SELECT COUNT(*) FROM despesa_fixa WHERE pago = 1")
            pagas = cursor.fetchone()[0]
            print(f"   - Pagas: {pagas}")
            print(f"   - Pendentes: {total - pagas}")
    
    # Verificar usuários
    if 'user' in tabelas:
        cursor.execute("SELECT COUNT(*) FROM user")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM user WHERE is_admin = 1")
        admins = cursor.fetchone()[0]
        print(f"\n👥 Usuários: {total_users}")
        print(f"   - Admins: {admins}")
    
    # Verificar famílias
    if 'familia' in tabelas:
        cursor.execute("SELECT COUNT(*) FROM familia")
        total_familias = cursor.fetchone()[0]
        print(f"\n👨‍👩‍👧‍👦 Famílias: {total_familias}")
    
    conn.close()
    
    print("\n" + "="*50)
    print("✅ Verificação concluída!")

if __name__ == '__main__':
    verificar_banco()
