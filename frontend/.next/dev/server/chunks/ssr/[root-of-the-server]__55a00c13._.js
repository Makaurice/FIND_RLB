module.exports = [
"[project]/frontend/pages/service/maintenance.tsx [ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Maintenance
]);
var __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__ = __turbopack_context__.i("[externals]/react/jsx-dev-runtime [external] (react/jsx-dev-runtime, cjs)");
var __TURBOPACK__imported__module__$5b$externals$5d2f$react__$5b$external$5d$__$28$react$2c$__cjs$29$__ = __turbopack_context__.i("[externals]/react [external] (react, cjs)");
;
;
function Maintenance() {
    const [requests, setRequests] = (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react__$5b$external$5d$__$28$react$2c$__cjs$29$__["useState"])([
        {
            id: 1,
            issue: 'Leaky faucet',
            priority: 'Medium',
            status: 'In Progress',
            date: '2026-02-18',
            provider: 'Home Fix Pro'
        },
        {
            id: 2,
            issue: 'Broken window latch',
            priority: 'High',
            status: 'Scheduled',
            date: '2026-02-20',
            provider: 'QuickRepairs'
        },
        {
            id: 3,
            issue: 'Paint touch-up',
            priority: 'Low',
            status: 'Completed',
            date: '2026-02-10',
            provider: 'Professional Paint'
        }
    ]);
    const [showRequestForm, setShowRequestForm] = (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react__$5b$external$5d$__$28$react$2c$__cjs$29$__["useState"])(false);
    const [newRequest, setNewRequest] = (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react__$5b$external$5d$__$28$react$2c$__cjs$29$__["useState"])({
        issue: '',
        priority: 'Medium',
        description: ''
    });
    const handleSubmitRequest = ()=>{
        if (newRequest.issue) {
            setRequests([
                ...requests,
                {
                    id: Date.now(),
                    issue: newRequest.issue,
                    priority: newRequest.priority,
                    status: 'Pending',
                    date: new Date().toISOString().split('T')[0],
                    provider: 'Awaiting Assignment'
                }
            ]);
            setNewRequest({
                issue: '',
                priority: 'Medium',
                description: ''
            });
            setShowRequestForm(false);
        }
    };
    const getPriorityColor = (priority)=>{
        switch(priority){
            case 'High':
                return '#F44336';
            case 'Medium':
                return '#FF9800';
            case 'Low':
                return '#4CAF50';
            default:
                return '#999';
        }
    };
    const getStatusColor = (status)=>{
        switch(status){
            case 'Completed':
                return '#4CAF50';
            case 'In Progress':
                return '#2196F3';
            case 'Scheduled':
                return '#FF9800';
            case 'Pending':
                return '#999';
            default:
                return '#999';
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
        style: {
            padding: 24,
            fontFamily: 'sans-serif'
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("h2", {
                children: "Maintenance Providers"
            }, void 0, false, {
                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                lineNumber: 48,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                style: {
                    backgroundColor: '#e8f5e9',
                    padding: 16,
                    marginBottom: 24,
                    borderRadius: 8
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("h3", {
                        children: "Report a Maintenance Issue"
                    }, void 0, false, {
                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                        lineNumber: 50,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("p", {
                        children: "Submit requests for repairs and maintenance. Our verified providers will respond within 24 hours."
                    }, void 0, false, {
                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                        lineNumber: 51,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                lineNumber: 49,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("button", {
                onClick: ()=>setShowRequestForm(!showRequestForm),
                style: {
                    fontSize: 16,
                    padding: 10,
                    marginBottom: 20,
                    backgroundColor: '#007bff',
                    color: 'white'
                },
                children: showRequestForm ? 'Cancel' : '+ New Maintenance Request'
            }, void 0, false, {
                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                lineNumber: 53,
                columnNumber: 7
            }, this),
            showRequestForm && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                style: {
                    border: '1px solid #ddd',
                    padding: 20,
                    marginBottom: 24,
                    borderRadius: 8,
                    backgroundColor: '#f9f9f9'
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                        style: {
                            marginBottom: 16
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("label", {
                                style: {
                                    display: 'block',
                                    marginBottom: 8,
                                    fontWeight: 'bold'
                                },
                                children: "Issue Type:"
                            }, void 0, false, {
                                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                lineNumber: 59,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("input", {
                                type: "text",
                                placeholder: "e.g., Leaky faucet, Broken window",
                                value: newRequest.issue,
                                onChange: (e)=>setNewRequest({
                                        ...newRequest,
                                        issue: e.target.value
                                    }),
                                style: {
                                    fontSize: 14,
                                    padding: 8,
                                    width: '100%'
                                }
                            }, void 0, false, {
                                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                lineNumber: 60,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                        lineNumber: 58,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                        style: {
                            marginBottom: 16
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("label", {
                                style: {
                                    display: 'block',
                                    marginBottom: 8,
                                    fontWeight: 'bold'
                                },
                                children: "Priority:"
                            }, void 0, false, {
                                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                lineNumber: 69,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("select", {
                                value: newRequest.priority,
                                onChange: (e)=>setNewRequest({
                                        ...newRequest,
                                        priority: e.target.value
                                    }),
                                style: {
                                    fontSize: 14,
                                    padding: 8,
                                    width: '100%'
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("option", {
                                        value: "Low",
                                        children: "Low"
                                    }, void 0, false, {
                                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                        lineNumber: 75,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("option", {
                                        value: "Medium",
                                        children: "Medium"
                                    }, void 0, false, {
                                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                        lineNumber: 76,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("option", {
                                        value: "High",
                                        children: "High"
                                    }, void 0, false, {
                                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                        lineNumber: 77,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                lineNumber: 70,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                        lineNumber: 68,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("div", {
                        style: {
                            marginBottom: 16
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("label", {
                                style: {
                                    display: 'block',
                                    marginBottom: 8,
                                    fontWeight: 'bold'
                                },
                                children: "Description:"
                            }, void 0, false, {
                                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                lineNumber: 81,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("textarea", {
                                placeholder: "Describe the issue in detail",
                                value: newRequest.description,
                                onChange: (e)=>setNewRequest({
                                        ...newRequest,
                                        description: e.target.value
                                    }),
                                style: {
                                    fontSize: 14,
                                    padding: 8,
                                    width: '100%',
                                    minHeight: 80
                                }
                            }, void 0, false, {
                                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                lineNumber: 82,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                        lineNumber: 80,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("button", {
                        onClick: handleSubmitRequest,
                        style: {
                            fontSize: 16,
                            padding: 10,
                            backgroundColor: '#28a745',
                            color: 'white'
                        },
                        children: "Submit Request"
                    }, void 0, false, {
                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                        lineNumber: 89,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                lineNumber: 57,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("h3", {
                children: "Maintenance History"
            }, void 0, false, {
                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                lineNumber: 92,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("table", {
                style: {
                    width: '100%',
                    borderCollapse: 'collapse'
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("thead", {
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("tr", {
                            style: {
                                backgroundColor: '#f0f0f0',
                                borderBottom: '2px solid #ccc'
                            },
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("th", {
                                    style: {
                                        textAlign: 'left',
                                        padding: 12
                                    },
                                    children: "Issue"
                                }, void 0, false, {
                                    fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                    lineNumber: 96,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("th", {
                                    style: {
                                        textAlign: 'left',
                                        padding: 12
                                    },
                                    children: "Priority"
                                }, void 0, false, {
                                    fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                    lineNumber: 97,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("th", {
                                    style: {
                                        textAlign: 'left',
                                        padding: 12
                                    },
                                    children: "Status"
                                }, void 0, false, {
                                    fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                    lineNumber: 98,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("th", {
                                    style: {
                                        textAlign: 'left',
                                        padding: 12
                                    },
                                    children: "Provider"
                                }, void 0, false, {
                                    fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                    lineNumber: 99,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("th", {
                                    style: {
                                        textAlign: 'left',
                                        padding: 12
                                    },
                                    children: "Date"
                                }, void 0, false, {
                                    fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                    lineNumber: 100,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/frontend/pages/service/maintenance.tsx",
                            lineNumber: 95,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                        lineNumber: 94,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("tbody", {
                        children: requests.map((r)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("tr", {
                                style: {
                                    borderBottom: '1px solid #eee'
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("td", {
                                        style: {
                                            padding: 12
                                        },
                                        children: r.issue
                                    }, void 0, false, {
                                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                        lineNumber: 106,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("td", {
                                        style: {
                                            padding: 12
                                        },
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("span", {
                                            style: {
                                                backgroundColor: getPriorityColor(r.priority),
                                                color: 'white',
                                                padding: '4 8',
                                                borderRadius: 4
                                            },
                                            children: r.priority
                                        }, void 0, false, {
                                            fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                            lineNumber: 108,
                                            columnNumber: 17
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                        lineNumber: 107,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("td", {
                                        style: {
                                            padding: 12
                                        },
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("span", {
                                            style: {
                                                backgroundColor: getStatusColor(r.status),
                                                color: 'white',
                                                padding: '4 8',
                                                borderRadius: 4
                                            },
                                            children: r.status
                                        }, void 0, false, {
                                            fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                            lineNumber: 113,
                                            columnNumber: 17
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                        lineNumber: 112,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("td", {
                                        style: {
                                            padding: 12
                                        },
                                        children: r.provider
                                    }, void 0, false, {
                                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                        lineNumber: 117,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$externals$5d2f$react$2f$jsx$2d$dev$2d$runtime__$5b$external$5d$__$28$react$2f$jsx$2d$dev$2d$runtime$2c$__cjs$29$__["jsxDEV"])("td", {
                                        style: {
                                            padding: 12
                                        },
                                        children: r.date
                                    }, void 0, false, {
                                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                        lineNumber: 118,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, r.id, true, {
                                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                                lineNumber: 105,
                                columnNumber: 13
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/frontend/pages/service/maintenance.tsx",
                        lineNumber: 103,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/frontend/pages/service/maintenance.tsx",
                lineNumber: 93,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/frontend/pages/service/maintenance.tsx",
        lineNumber: 47,
        columnNumber: 5
    }, this);
}
}),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__55a00c13._.js.map