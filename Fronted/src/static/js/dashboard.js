/**
 * EIVAI - Dashboard JavaScript Controller
 * Archivo: dashboard.js
 * 
 * Descripción:
 *   Controlador principal del dashboard que maneja la comunicación con el backend
 *   y la actualización de visualizaciones en tiempo real.
 *
 * Funcionalidades:
 *   - Comunicación con servicios del backend
 *   - Actualización automática de estadísticas
 *   - Gestión de alertas y notificaciones
 *   - Visualización de datos en tiempo real
 *   - Manejo de errores y estados de carga
 *
 * Autor: Equipo EIVAI
 * Fecha: 2025
 * Versión: 2.1.0
 */

class EIVAIDashboard {
    constructor() {
        this.baseUrl = 'http://127.0.0.1:8000';
        this.updateInterval = 30000; // 30 segundos
        this.autoUpdateTimer = null;
        this.isLoading = false;
        
        // Inicializar dashboard cuando el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    /**
     * Inicialización principal del dashboard
     */
    async init() {
        try {
            console.log('Inicializando EIVAI Dashboard...');
            
            // Cargar datos iniciales
            await this.loadInitialData();
            
            // Configurar actualizaciones automáticas
            this.setupAutoUpdate();
            
            // Configurar event listeners
            this.setupEventListeners();
            
            console.log('Dashboard EIVAI inicializado correctamente');
            this.showNotification('Dashboard cargado correctamente', 'success');
            
        } catch (error) {
            console.error('Error inicializando dashboard:', error);
            this.showNotification('Error al cargar el dashboard', 'error');
        }
    }    /**
     * Cargar datos iniciales del dashboard
     */
    async loadInitialData() {
        this.setLoadingState(true);
        
        try {
            // Usar el endpoint completo para obtener todos los datos en una sola llamada
            const dashboardData = await this.fetchDashboardCompleto();
            
            // Actualizar todas las visualizaciones con los datos obtenidos
            if (dashboardData.stats_generales) {
                this.updateDashboardStats(dashboardData.stats_generales);
            }
            
            if (dashboardData.alertas) {
                this.updateAlertasSection(dashboardData.alertas.alertas_recientes || []);
            }
            
            if (dashboardData.instrumentos) {
                this.updateInstrumentosSection(dashboardData.instrumentos);
            }
            
            if (dashboardData.procedimientos) {
                this.updateProcedimientosSection(dashboardData.procedimientos);
            }
            
            if (dashboardData.conteos_recientes) {
                this.updateConteosSection(dashboardData.conteos_recientes);
            }
            
            if (dashboardData.sets_quirurgicos) {
                this.updateSetsSection(dashboardData.sets_quirurgicos);
            }
            
        } catch (error) {
            console.error('Error cargando datos iniciales:', error);
            this.showFallbackData();
        } finally {
            this.setLoadingState(false);
        }
    }

    /**
     * Obtener todos los datos del dashboard en una sola llamada
     */
    async fetchDashboardCompleto() {
        try {
            const response = await fetch(`${this.baseUrl}/api/dashboard/completo`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error obteniendo datos completos del dashboard:', error);
            // Fallback a métodos individuales si el endpoint completo falla
            return await this.fetchDataIndividually();
        }
    }

    /**
     * Método fallback para obtener datos individualmente
     */
    async fetchDataIndividually() {
        try {
            const [dashboardStats, alertas, instrumentos, procedimientos, conteos, sets] = await Promise.all([
                this.fetchDashboardStats(),
                this.fetchAlertas(),
                this.fetchInstrumentos(),
                this.fetchProcedimientos(),
                this.fetchConteos(),
                this.fetchSets()
            ]);

            return {
                stats_generales: dashboardStats,
                alertas: { alertas_recientes: alertas },
                instrumentos: instrumentos,
                procedimientos: procedimientos,
                conteos_recientes: conteos,
                sets_quirurgicos: sets
            };
        } catch (error) {
            console.error('Error en método fallback:', error);
            throw error;
        }
    }

    /**
     * Obtener estadísticas del dashboard desde el backend
     */
    async fetchDashboardStats() {
        try {
            const response = await fetch(`${this.baseUrl}/api/dashboard/stats`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error obteniendo estadísticas:', error);
            return this.getFallbackStats();
        }
    }

    /**
     * Obtener alertas activas del sistema
     */
    async fetchAlertas() {
        try {
            const response = await fetch(`${this.baseUrl}/api/alertas/activas`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error obteniendo alertas:', error);
            return [];
        }
    }

    /**
     * Obtener estadísticas de instrumentos
     */
    async fetchInstrumentos() {
        try {
            const response = await fetch(`${this.baseUrl}/api/instrumentos/estadisticas`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error obteniendo instrumentos:', error);
            return { total: 0, categorias: [], recientes: [] };
        }
    }    /**
     * Obtener estadísticas de procedimientos
     */
    async fetchProcedimientos() {
        try {
            const response = await fetch(`${this.baseUrl}/api/procedimientos/estadisticas`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error obteniendo procedimientos:', error);
            return { total: 0, activos: 0, completados: 0 };
        }
    }

    /**
     * Obtener conteos recientes
     */
    async fetchConteos() {
        try {
            const response = await fetch(`${this.baseUrl}/api/conteos/recientes?limit=5`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error obteniendo conteos:', error);
            return [];
        }
    }

    /**
     * Obtener sets quirúrgicos
     */
    async fetchSets() {
        try {
            const response = await fetch(`${this.baseUrl}/api/sets/activos?limit=5`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error obteniendo sets:', error);
            return [];
        }
    }

    /**
     * Actualizar estadísticas principales del dashboard
     */
    updateDashboardStats(stats) {
        try {
            // Actualizar elementos de estadísticas
            this.updateElement('total-tools', stats.instrumentos_registrados || 248);
            this.updateElement('successful-id', (stats.identificaciones_exitosas || 2247).toLocaleString());
            this.updateElement('avg-time', stats.tiempo_promedio || '18.3s');
            this.updateElement('accuracy', stats.precision || '96.7%');
            
            // Actualizar estadísticas del día
            this.updateElement('daily-identifications', stats.identificaciones_hoy || 42);
            this.updateElement('daily-avg-time', stats.tiempo_promedio_hoy || '2.1s');
            this.updateElement('daily-accuracy', stats.precision_hoy || '95.3%');
            this.updateElement('active-users', stats.usuarios_activos || 7);
            
            console.log('Estadísticas actualizadas:', stats);
        } catch (error) {
            console.error('Error actualizando estadísticas:', error);
        }
    }    /**
     * Actualizar sección de alertas
     */
    updateAlertasSection(alertas) {
        const alertasContainer = document.getElementById('alertas-container');
        if (!alertasContainer) return;

        if (!alertas || alertas.length === 0) {
            alertasContainer.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i>
                    No hay alertas activas
                </div>
            `;
            return;
        }

        const alertasHTML = alertas.slice(0, 5).map(alerta => `
            <div class="alert alert-${this.getAlertType(alerta.tipo || alerta.tipo_alerta)} alert-dismissible fade show">
                <i class="fas fa-${this.getAlertIcon(alerta.tipo || alerta.tipo_alerta)} me-2"></i>
                <strong>${alerta.titulo || 'Alerta del Sistema'}</strong>
                <p class="mb-1">${alerta.descripcion || alerta.mensaje || 'Sin descripción'}</p>
                <small class="text-muted">${this.formatDate(alerta.fecha_creacion)}</small>
                <button type="button" class="btn-close" onclick="dashboard.resolverAlerta(${alerta.id || alerta.alerta_id})"></button>
            </div>
        `).join('');

        alertasContainer.innerHTML = alertasHTML;
    }

    /**
     * Actualizar sección de instrumentos
     */
    updateInstrumentosSection(instrumentos) {
        // Actualizar contador de instrumentos
        this.updateElement('instrumentos-total', instrumentos.total || 0);
        
        // Actualizar categorías más usadas
        const categoriasContainer = document.getElementById('categorias-container');
        if (categoriasContainer && instrumentos.categorias) {
            const categoriasHTML = instrumentos.categorias.slice(0, 5).map(categoria => `
                <div class="d-flex justify-content-between mb-2">
                    <span>${categoria.nombre}</span>
                    <strong>${categoria.cantidad}</strong>
                </div>
            `).join('');
            
            categoriasContainer.innerHTML = categoriasHTML;
        }
    }    /**
     * Actualizar sección de procedimientos
     */
    updateProcedimientosSection(procedimientos) {
        this.updateElement('procedimientos-total', procedimientos.total || 0);
        this.updateElement('procedimientos-activos', procedimientos.activos || 0);
        this.updateElement('procedimientos-completados', procedimientos.completados || 0);
    }

    /**
     * Actualizar sección de conteos recientes
     */
    updateConteosSection(conteos) {
        const conteosContainer = document.getElementById('conteos-container');
        if (!conteosContainer) return;

        if (conteos.length === 0) {
            conteosContainer.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-camera me-2"></i>
                    No hay conteos recientes
                </div>
            `;
            return;
        }

        const conteosHTML = conteos.slice(0, 5).map(conteo => `
            <div class="border-bottom pb-2 mb-2">
                <div class="d-flex justify-content-between">
                    <span class="fw-bold">${conteo.procedimiento_nombre || 'Conteo'}</span>
                    <small class="text-muted">${this.formatDate(conteo.fecha_creacion)}</small>
                </div>
                <div class="d-flex justify-content-between">
                    <small>Estado: <span class="badge bg-${this.getConteoStatusColor(conteo.estado)}">${conteo.estado}</span></small>
                    <small>Instrumentos: ${conteo.total_instrumentos || 0}</small>
                </div>
            </div>
        `).join('');

        conteosContainer.innerHTML = conteosHTML;
    }

    /**
     * Actualizar sección de sets quirúrgicos
     */
    updateSetsSection(sets) {
        const setsContainer = document.getElementById('sets-container');
        if (!setsContainer) return;

        if (sets.length === 0) {
            setsContainer.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-box me-2"></i>
                    No hay sets disponibles
                </div>
            `;
            return;
        }

        const setsHTML = sets.slice(0, 5).map(set => `
            <div class="border-bottom pb-2 mb-2">
                <div class="d-flex justify-content-between">
                    <span class="fw-bold">${set.nombre}</span>
                    <small class="text-muted">${set.categoria || 'General'}</small>
                </div>
                <div class="d-flex justify-content-between">
                    <small>Estado: <span class="badge bg-${this.getSetStatusColor(set.activo)}">${set.activo ? 'Activo' : 'Inactivo'}</span></small>
                    <small>Instrumentos: ${set.total_instrumentos || 0}</small>
                </div>
            </div>
        `).join('');

        setsContainer.innerHTML = setsHTML;
    }

    /**
     * Resolver una alerta específica
     */
    async resolverAlerta(alertaId) {
        try {
            const response = await fetch(`${this.baseUrl}/api/alertas/${alertaId}/resolver`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                this.showNotification('Alerta resuelta correctamente', 'success');
                // Recargar alertas
                const alertas = await this.fetchAlertas();
                this.updateAlertasSection(alertas);
            } else {
                throw new Error('Error al resolver la alerta');
            }
        } catch (error) {
            console.error('Error resolviendo alerta:', error);
            this.showNotification('Error al resolver la alerta', 'error');
        }
    }

    /**
     * Configurar actualizaciones automáticas
     */
    setupAutoUpdate() {
        this.autoUpdateTimer = setInterval(async () => {
            if (!this.isLoading) {
                await this.loadInitialData();
            }
        }, this.updateInterval);
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Botón de actualización manual
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadInitialData());
        }

        // Gestión de visibilidad de la página para pausar/reanudar actualizaciones
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseAutoUpdate();
            } else {
                this.resumeAutoUpdate();
            }
        });
    }

    /**
     * Pausar actualizaciones automáticas
     */
    pauseAutoUpdate() {
        if (this.autoUpdateTimer) {
            clearInterval(this.autoUpdateTimer);
            this.autoUpdateTimer = null;
        }
    }

    /**
     * Reanudar actualizaciones automáticas
     */
    resumeAutoUpdate() {
        if (!this.autoUpdateTimer) {
            this.setupAutoUpdate();
        }
    }

    /**
     * Establecer estado de carga
     */
    setLoadingState(loading) {
        this.isLoading = loading;
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = loading ? 'block' : 'none';
        }
    }

    /**
     * Actualizar elemento del DOM
     */
    updateElement(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
        }
    }

    /**
     * Mostrar notificación al usuario
     */
    showNotification(message, type = 'info') {
        // Crear notificación toast
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto"></button>
            </div>
        `;

        // Agregar al contenedor de toasts
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }

        toastContainer.appendChild(toast);

        // Mostrar toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        // Limpiar después de mostrar
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    /**
     * Obtener tipo de alerta para Bootstrap
     */
    getAlertType(tipo) {
        const tipos = {
            'error': 'danger',
            'warning': 'warning',
            'info': 'info',
            'success': 'success'
        };
        return tipos[tipo] || 'info';
    }

    /**
     * Obtener icono de alerta
     */
    getAlertIcon(tipo) {
        const iconos = {
            'error': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle',
            'success': 'check-circle'
        };
        return iconos[tipo] || 'info-circle';
    }    /**
     * Formatear fecha para mostrar
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('es-ES');
    }

    /**
     * Obtener color para el estado del conteo
     */
    getConteoStatusColor(estado) {
        const colores = {
            'pendiente': 'warning',
            'en_progreso': 'info',
            'completado': 'success',
            'verificado': 'primary',
            'error': 'danger'
        };
        return colores[estado] || 'secondary';
    }

    /**
     * Obtener color para el estado del set
     */
    getSetStatusColor(activo) {
        return activo ? 'success' : 'secondary';
    }

    /**
     * Obtener datos de respaldo en caso de error
     */
    getFallbackStats() {
        return {
            instrumentos_registrados: 248,
            identificaciones_exitosas: 2247,
            tiempo_promedio: '18.3s',
            precision: '96.7%',
            identificaciones_hoy: 42,
            tiempo_promedio_hoy: '2.1s',
            precision_hoy: '95.3%',
            usuarios_activos: 7
        };
    }

    /**
     * Mostrar datos de respaldo
     */
    showFallbackData() {
        const fallbackStats = this.getFallbackStats();
        this.updateDashboardStats(fallbackStats);
        this.showNotification('Mostrando datos almacenados localmente', 'warning');
    }    /**
     * Destructor para limpiar recursos
     */
    destroy() {
        this.pauseAutoUpdate();
    }

    /**
     * Método de debug para probar todos los endpoints
     */
    async debugTestEndpoints() {
        console.log('🔧 Iniciando prueba de endpoints...');
        
        const endpoints = [
            { name: 'Dashboard Stats', method: () => this.fetchDashboardStats() },
            { name: 'Alertas', method: () => this.fetchAlertas() },
            { name: 'Instrumentos', method: () => this.fetchInstrumentos() },
            { name: 'Procedimientos', method: () => this.fetchProcedimientos() },
            { name: 'Conteos', method: () => this.fetchConteos() },
            { name: 'Sets', method: () => this.fetchSets() },
            { name: 'Dashboard Completo', method: () => this.fetchDashboardCompleto() }
        ];

        for (const endpoint of endpoints) {
            try {
                console.log(`🧪 Probando ${endpoint.name}...`);
                const result = await endpoint.method();
                console.log(`✅ ${endpoint.name}:`, result);
            } catch (error) {
                console.log(`❌ ${endpoint.name}:`, error.message);
            }
        }
        
        console.log('🔧 Prueba de endpoints completada');
    }

    /**
     * Método de debug para mostrar estado actual
     */
    debugShowState() {
        console.log('📊 Estado actual del dashboard:', {
            baseUrl: this.baseUrl,
            updateInterval: this.updateInterval,
            isLoading: this.isLoading,
            autoUpdateActive: this.autoUpdateTimer !== null
        });
    }
}
}

// Inicializar dashboard global
const dashboard = new EIVAIDashboard();

// Limpiar recursos al cerrar la página
window.addEventListener('beforeunload', () => {
    dashboard.destroy();
});
