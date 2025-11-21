"""
Sistema de Monetização - Preparado para o Futuro
Este arquivo contém funções para quando você quiser ativar a monetização
"""
from datetime import datetime, timedelta

# Configuração de Planos
PLANOS = {
    'free': {
        'nome': 'Gratuito',
        'preco': 0,
        'max_usuarios': 2,
        'max_meses_historico': 6,
        'exportar_relatorios': False,
        'graficos_avancados': False,
        'alertas_personalizados': False,
        'backup_nuvem': False,
        'suporte_prioritario': False,
    },
    'premium': {
        'nome': 'Premium',
        'preco': 4.99,
        'max_usuarios': 10,
        'max_meses_historico': -1,  # Ilimitado
        'exportar_relatorios': True,
        'graficos_avancados': True,
        'alertas_personalizados': True,
        'backup_nuvem': True,
        'suporte_prioritario': True,
    },
    'vip': {
        'nome': 'VIP',
        'preco': 9.99,
        'max_usuarios': -1,  # Ilimitado
        'max_meses_historico': -1,  # Ilimitado
        'exportar_relatorios': True,
        'graficos_avancados': True,
        'alertas_personalizados': True,
        'backup_nuvem': True,
        'suporte_prioritario': True,
        'integracao_bancos': True,
        'app_mobile': True,
    }
}

def verificar_acesso_funcionalidade(familia, funcionalidade):
    """
    Verifica se a família tem acesso a uma funcionalidade
    
    Por enquanto, retorna sempre True (tudo liberado)
    Quando ativar monetização, descomentar a lógica
    """
    # TODO: Ativar quando começar a monetizar
    # if familia.plano == 'free':
    #     return PLANOS['free'].get(funcionalidade, False)
    # elif familia.plano == 'premium':
    #     return PLANOS['premium'].get(funcionalidade, True)
    # elif familia.plano == 'vip':
    #     return True
    
    # Por enquanto, tudo liberado
    return True

def verificar_plano_ativo(familia):
    """
    Verifica se o plano premium está ativo
    
    Por enquanto, retorna sempre True
    Quando ativar monetização, verificar data_expiracao
    """
    # TODO: Ativar quando começar a monetizar
    # if familia.plano == 'free':
    #     return True
    # 
    # if familia.data_expiracao is None:
    #     return False
    # 
    # return datetime.now() < familia.data_expiracao
    
    # Por enquanto, tudo ativo
    return True

def upgrade_plano(familia, plano, meses=1):
    """
    Faz upgrade do plano da família
    
    Uso futuro:
    upgrade_plano(familia, 'premium', meses=12)
    """
    from app import db
    
    familia.plano = plano
    
    if plano != 'free':
        if familia.data_expiracao and familia.data_expiracao > datetime.now():
            # Estender plano existente
            familia.data_expiracao += timedelta(days=30 * meses)
        else:
            # Novo plano
            familia.data_expiracao = datetime.now() + timedelta(days=30 * meses)
    
    familia.max_usuarios = PLANOS[plano]['max_usuarios']
    familia.funcionalidades_premium = True
    
    db.session.commit()
    return True

def downgrade_plano_expirado(familia):
    """
    Faz downgrade automático quando o plano expira
    
    Executar diariamente via cron job
    """
    from app import db
    
    if familia.plano != 'free' and familia.data_expiracao:
        if datetime.now() > familia.data_expiracao:
            familia.plano = 'free'
            familia.max_usuarios = PLANOS['free']['max_usuarios']
            familia.funcionalidades_premium = False
            db.session.commit()
            return True
    
    return False

def calcular_receita_mensal():
    """
    Calcula receita mensal total
    
    Para dashboard admin
    """
    from app import Familia
    
    familias_premium = Familia.query.filter(
        Familia.plano.in_(['premium', 'vip']),
        Familia.data_expiracao > datetime.now()
    ).all()
    
    receita = 0
    for f in familias_premium:
        receita += PLANOS[f.plano]['preco']
    
    return receita

def estatisticas_planos():
    """
    Retorna estatísticas de planos
    
    Para dashboard admin
    """
    from app import Familia
    
    total = Familia.query.count()
    free = Familia.query.filter_by(plano='free').count()
    premium = Familia.query.filter_by(plano='premium').count()
    vip = Familia.query.filter_by(plano='vip').count()
    
    return {
        'total': total,
        'free': free,
        'premium': premium,
        'vip': vip,
        'taxa_conversao': ((premium + vip) / total * 100) if total > 0 else 0,
        'receita_mensal': calcular_receita_mensal()
    }

# Funcionalidades Premium (para implementar no futuro)
FUNCIONALIDADES_PREMIUM = {
    'exportar_pdf': {
        'nome': 'Exportar Relatórios PDF',
        'descricao': 'Exporte seus relatórios financeiros em PDF',
        'plano_minimo': 'premium'
    },
    'exportar_excel': {
        'nome': 'Exportar para Excel',
        'descricao': 'Exporte seus dados para planilhas Excel',
        'plano_minimo': 'premium'
    },
    'graficos_avancados': {
        'nome': 'Gráficos Avançados',
        'descricao': 'Acesse gráficos e análises avançadas',
        'plano_minimo': 'premium'
    },
    'alertas_whatsapp': {
        'nome': 'Alertas no WhatsApp',
        'descricao': 'Receba alertas de gastos no WhatsApp',
        'plano_minimo': 'premium'
    },
    'backup_nuvem': {
        'nome': 'Backup na Nuvem',
        'descricao': 'Backup automático no Google Drive',
        'plano_minimo': 'premium'
    },
    'previsoes_ia': {
        'nome': 'Previsões com IA',
        'descricao': 'Previsões inteligentes de gastos',
        'plano_minimo': 'vip'
    },
    'integracao_bancos': {
        'nome': 'Integração com Bancos',
        'descricao': 'Sincronize automaticamente com seu banco',
        'plano_minimo': 'vip'
    },
    'app_mobile': {
        'nome': 'App Mobile',
        'descricao': 'Acesso ao app mobile iOS e Android',
        'plano_minimo': 'vip'
    }
}

# Preços especiais (para campanhas futuras)
PRECOS_ESPECIAIS = {
    'founder': {
        'nome': 'Founder Plan',
        'descricao': 'Primeiros 100 usuários',
        'preco': 2.99,
        'plano': 'premium',
        'vitalicio': True
    },
    'anual': {
        'nome': 'Plano Anual',
        'descricao': '12 meses pelo preço de 10',
        'preco': 49.90,
        'plano': 'premium',
        'meses': 12
    },
    'vitalicio': {
        'nome': 'Acesso Vitalício',
        'descricao': 'Pagamento único, acesso para sempre',
        'preco': 149.00,
        'plano': 'premium',
        'vitalicio': True
    }
}
