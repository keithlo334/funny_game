import ui
import os

# 創建 WebView 實例
webview = ui.WebView()

# 定義完整的 HTML 內容,包含 SVG 命名空間
html_content = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>速成打字冒險</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#4F46E5',
                        secondary: '#EC4899',
                        success: '#10B981',
                        warning: '#F59E0B',
                        danger: '#EF4444',
                        background: '#F0F9FF',
                        darkBg: '#111827'
                    },
                    animation: {
                        'bounce-slow': 'bounce 2s infinite',
                        'float': 'float 3s ease-in-out infinite',
                        'slide-in': 'slideIn 0.5s ease-out forwards',
                        'fade-in': 'fadeIn 0.5s ease-out forwards',
                        'scale-in': 'scaleIn 0.3s ease-out forwards',
                        'rotate-slow': 'rotate 8s linear infinite'
                    },
                    keyframes: {
                        float: {
                            '0%, 100%': { transform: 'translateY(0)' },
                            '50%': { transform: 'translateY(-10px)' }
                        },
                        slideIn: {
                            '0%': { transform: 'translateY(20px)', opacity: 0 },
                            '100%': { transform: 'translateY(0)', opacity: 1 }
                        },
                        fadeIn: {
                            '0%': { opacity: 0 },
                            '100%': { opacity: 1 }
                        },
                        scaleIn: {
                            '0%': { transform: 'scale(0.8)', opacity: 0 },
                            '100%': { transform: 'scale(1)', opacity: 1 }
                        }
                    }
                }
            },
            darkMode: 'class'
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700&display=swap');
        
        body {
            font-family: 'Baloo 2', cursive;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }
        
        /* 確保hidden類正確工作 */
        .hidden {
            display: none !important;
        }
        
        /* 禁止選擇文字 */
        .no-select {
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        /* 單詞動畫 */
        @keyframes wordDrop {
            0% { transform: translateY(-100%); opacity: 0; }
            10% { opacity: 1; }
            100% { transform: translateY(var(--drop-distance)); opacity: 1; }
        }
        
        .word-drop {
            animation: wordDrop var(--drop-time) linear forwards;
            position: absolute;
            top: 0;
            border-radius: 1rem;
            padding: 0.5rem 1rem;
            font-weight: 600;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        /* 消除單詞動畫 */
        @keyframes wordRemove {
            0% { transform: scale(1); opacity: 1; }
            100% { transform: scale(1.5); opacity: 0; }
        }
        
        .word-remove {
            animation: wordRemove 0.5s ease-out forwards;
        }
        
        /* 星星動畫 */
        @keyframes star {
            0% { transform: scale(0) rotate(0deg); opacity: 0; }
            50% { transform: scale(1) rotate(180deg); opacity: 1; }
            100% { transform: scale(0) rotate(360deg); opacity: 0; }
        }
        
        .star {
            position: absolute;
            width: 20px;
            height: 20px;
            background-color: gold;
            clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
            animation: star 1s ease-out forwards;
        }
        
        /* 獎盃發光動畫 */
        @keyframes glow {
            0%, 100% { filter: drop-shadow(0 0 5px gold); }
            50% { filter: drop-shadow(0 0 15px gold); }
        }
        
        .trophy-glow {
            animation: glow 2s infinite;
        }
        
        /* 煙火爆炸 */
        @keyframes explode {
            0% { transform: scale(0); opacity: 1; }
            100% { transform: scale(1); opacity: 0; }
        }
        
        .firework {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            animation: explode 0.8s cubic-bezier(0, 0.5, 0.5, 1) forwards;
        }
        
        /* 進度條動畫 */
        @keyframes progressFill {
            from { width: 0; }
            to { width: 100%; }
        }
        
        .progress-fill {
            animation: progressFill var(--level-duration) linear forwards;
        }
        
        /* 打字指示器 */
        .hint-char {
            display: inline-block;
            position: relative;
        }
        
        .hint-char.active::after {
            content: '';
            position: absolute;
            left: 0;
            right: 0;
            bottom: -2px;
            height: 3px;
            background-color: currentColor;
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        /* 彈出提示動畫 */
        @keyframes popUp {
            0% { transform: scale(0.8); opacity: 0; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .pop-animation {
            animation: popUp 0.5s ease-out forwards;
        }
        
        /* iPhone輸入優化 */
        input {
            font-size: 16px; /* 防止iOS縮放 */
        }
    </style>
</head>
<body class="bg-background dark:bg-darkBg min-h-screen text-gray-800 dark:text-gray-100 overflow-x-hidden">
    <!-- 主遊戲容器 -->
    <div class="relative flex flex-col min-h-screen">
        <!-- 開始界面 -->
        <div id="startScreen" class="fixed inset-0 bg-background dark:bg-darkBg z-50 flex flex-col items-center justify-center p-4 animate-fade-in">
            <h1 class="text-5xl md:text-6xl font-bold text-primary mb-8 text-center">速成打字冒險</h1>
            <div class="relative w-64 h-64 mb-6 animate-float">
                <!-- 卡通宇航員 -->
                <svg class="w-full h-full" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <!-- 宇航員頭盔 -->
                    <circle cx="100" cy="80" r="40" fill="#E0E7FF" stroke="#4F46E5" stroke-width="3"/>
                    <circle cx="85" cy="70" r="5" fill="#4F46E5"/>
                    <circle cx="115" cy="70" r="5" fill="#4F46E5"/>
                    <path d="M90 90 Q100 100 110 90" stroke="#4F46E5" stroke-width="3" stroke-linecap="round"/>
                    
                    <!-- 宇航員身體 -->
                    <rect x="70" y="120" width="60" height="60" rx="10" fill="#4F46E5"/>
                    <rect x="80" y="100" width="40" height="30" rx="10" fill="#E0E7FF" stroke="#4F46E5" stroke-width="3"/>
                    
                    <!-- 宇航員手臂 -->
                    <rect x="40" y="130" width="30" height="15" rx="7.5" fill="#6366F1" transform="rotate(20 40 130)"/>
                    <rect x="130" y="130" width="30" height="15" rx="7.5" fill="#6366F1" transform="rotate(-20 130 130)"/>
                    
                    <!-- 宇航員腿 -->
                    <rect x="75" y="180" width="20" height="30" rx="7" fill="#6366F1" transform="rotate(-5 75 180)"/>
                    <rect x="105" y="180" width="20" height="30" rx="7" fill="#6366F1" transform="rotate(5 105 180)"/>
                    
                    <!-- 星星裝飾 -->
                    <path d="M160 40 L163 47 L170 50 L163 53 L160 60 L157 53 L150 50 L157 47 Z" fill="#FCD34D"/>
                    <path d="M40 60 L43 67 L50 70 L43 73 L40 80 L37 73 L30 70 L37 67 Z" fill="#FCD34D"/>
                    <path d="M140 170 L143 177 L150 180 L143 183 L140 190 L137 183 L130 180 L137 177 Z" fill="#FCD34D"/>
                </svg>
            </div>
            
            <div class="flex flex-col w-full max-w-md gap-4">
                <button id="startBtn" class="bg-primary hover:bg-primary/90 text-white font-bold py-4 px-8 rounded-xl text-xl shadow-lg transform transition hover:scale-105">
                    開始冒險
                </button>
                <button id="tutorialBtn" class="bg-secondary hover:bg-secondary/90 text-white font-bold py-4 px-8 rounded-xl text-xl shadow-lg transform transition hover:scale-105">
                    遊戲教學
                </button>
            </div>
        </div>
        
        <!-- 教學界面 -->
        <div id="tutorialScreen" class="fixed inset-0 bg-background dark:bg-darkBg z-40 flex flex-col items-center justify-center p-6 hidden">
            <h2 class="text-3xl font-bold text-primary mb-6">如何遊玩</h2>
            
            <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg max-w-md w-full">
                <div class="space-y-4">
                    <div class="flex items-start gap-3">
                        <div class="bg-primary text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">1</div>
                        <p class="text-lg">單詞會從上方落下,速度會隨著關卡提升</p>
                    </div>
                    <div class="flex items-start gap-3">
                        <div class="bg-primary text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">2</div>
                        <p class="text-lg">在輸入框中打出對應的單詞</p>
                    </div>
                    <div class="flex items-start gap-3">
                        <div class="bg-primary text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">3</div>
                        <p class="text-lg">單詞被消除後獲得分數</p>
                    </div>
                    <div class="flex items-start gap-3">
                        <div class="bg-primary text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">4</div>
                        <p class="text-lg">達到目標分數即可過關!</p>
                    </div>
                    <div class="flex items-start gap-3">
                        <div class="bg-primary text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">5</div>
                        <p class="text-lg">如果有單詞落到底部,遊戲就結束了</p>
                    </div>
                </div>
                
                <button id="closeTutorialBtn" class="mt-6 bg-primary hover:bg-primary/90 text-white font-bold py-3 px-6 rounded-xl w-full text-lg shadow-md transform transition hover:scale-105">
                    了解了!
                </button>
            </div>
        </div>
        
        <!-- 關卡選擇 -->
        <div id="levelSelect" class="fixed inset-0 bg-background dark:bg-darkBg z-30 flex flex-col p-6 hidden">
            <h2 class="text-3xl font-bold text-primary mb-6 text-center">選擇關卡</h2>
            
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4 overflow-y-auto pb-20">
                <!-- 關卡1 -->
                <button class="level-button bg-white dark:bg-gray-800 rounded-2xl p-4 flex flex-col items-center shadow-md transform transition hover:scale-105" data-level="1">
                    <div class="level-number bg-primary text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mb-2">1</div>
                    <h3 class="text-lg font-bold">新手村</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">簡單單詞</p>
                    <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="level-progress bg-success h-full rounded-full" style="width: 0%"></div>
                    </div>
                </button>
                
                <!-- 關卡2 -->
                <button class="level-button bg-white dark:bg-gray-800 rounded-2xl p-4 flex flex-col items-center shadow-md transform transition hover:scale-105 opacity-60" data-level="2" disabled>
                    <div class="level-number bg-gray-400 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mb-2">2</div>
                    <h3 class="text-lg font-bold">進階森林</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">中等單詞</p>
                    <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="level-progress bg-success h-full rounded-full" style="width: 0%"></div>
                    </div>
                </button>
                
                <!-- 關卡3 -->
                <button class="level-button bg-white dark:bg-gray-800 rounded-2xl p-4 flex flex-col items-center shadow-md transform transition hover:scale-105 opacity-60" data-level="3" disabled>
                    <div class="level-number bg-gray-400 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mb-2">3</div>
                    <h3 class="text-lg font-bold">挑戰高原</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">較長單詞</p>
                    <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="level-progress bg-success h-full rounded-full" style="width: 0%"></div>
                    </div>
                </button>
                
                <!-- 關卡4 -->
                <button class="level-button bg-white dark:bg-gray-800 rounded-2xl p-4 flex flex-col items-center shadow-md transform transition hover:scale-105 opacity-60" data-level="4" disabled>
                    <div class="level-number bg-gray-400 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mb-2">4</div>
                    <h3 class="text-lg font-bold">拼音海洋</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">注音練習</p>
                    <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="level-progress bg-success h-full rounded-full" style="width: 0%"></div>
                    </div>
                </button>
                
                <!-- 關卡5 -->
                <button class="level-button bg-white dark:bg-gray-800 rounded-2xl p-4 flex flex-col items-center shadow-md transform transition hover:scale-105 opacity-60" data-level="5" disabled>
                    <div class="level-number bg-gray-400 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mb-2">5</div>
                    <h3 class="text-lg font-bold">太空站</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">英文單詞</p>
                    <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="level-progress bg-success h-full rounded-full" style="width: 0%"></div>
                    </div>
                </button>
            </div>
            
            <button id="backFromLevelsBtn" class="absolute bottom-6 left-6 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-full p-3 shadow-md transform transition hover:scale-105">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
            </button>
        </div>
        
        <!-- 遊戲界面 -->
        <div id="gameScreen" class="flex-1 flex flex-col hidden">
            <!-- 頂部狀態欄 -->
            <div class="sticky top-0 z-10 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm p-4 shadow-md">
                <div class="flex justify-between items-center mb-2">
                    <div class="flex items-center gap-2">
                        <button id="pauseButton" class="text-primary p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </button>
                        <span class="font-bold text-lg">關卡 <span id="currentLevel">1</span></span>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="flex items-center gap-1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118l-2.8-2.034c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                            <span id="scoreDisplay" class="font-bold">0</span>
                        </div>
                    </div>
                </div>
                
                <!-- 進度條 -->
                <div class="relative h-4 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div id="levelProgressBar" class="h-full bg-success" style="width: 0%"></div>
                    <div id="levelTarget" class="absolute right-0 top-0 h-full w-1 bg-warning"></div>
                </div>
            </div>
            
            <!-- 遊戲區域 -->
            <div id="gameArea" class="flex-1 relative overflow-hidden">
                <!-- 這裡會動態生成掉落的單詞 -->
            </div>
            
            <!-- 底部輸入區 -->
            <div class="sticky bottom-0 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm p-4 shadow-md">
                <div class="max-w-md mx-auto">
                    <div id="typingHint" class="text-center mb-2 text-xl font-bold tracking-wide h-8"></div>
                    <input 
                        type="text" 
                        id="wordInput" 
                        class="w-full p-4 text-xl border-2 border-primary rounded-xl focus:outline-none focus:ring-2 focus:ring-primary bg-white dark:bg-gray-900 text-gray-800 dark:text-white"
                        placeholder="在這裡輸入..."
                        autocomplete="off"
                        autocapitalize="off"
                        autocorrect="off"
                    >
                </div>
            </div>
        </div>
        
        <!-- 暫停界面 -->
        <div id="pauseScreen" class="fixed inset-0 z-20 bg-black/70 flex items-center justify-center p-6 hidden">
            <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 max-w-sm w-full animate-scale-in">
                <h2 class="text-3xl font-bold text-primary mb-6 text-center">遊戲暫停</h2>
                
                <div class="space-y-4">
                    <button id="resumeButton" class="w-full bg-primary hover:bg-primary/90 text-white font-bold py-3 px-6 rounded-xl text-lg shadow-md transform transition hover:scale-105">
                        繼續遊戲
                    </button>
                    <button id="restartLevelButton" class="w-full bg-warning hover:bg-warning/90 text-white font-bold py-3 px-6 rounded-xl text-lg shadow-md transform transition hover:scale-105">
                        重新開始
                    </button>
                    <button id="quitToMenuButton" class="w-full bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-xl text-lg shadow-md transform transition hover:scale-105">
                        返回選單
                    </button>
                </div>
            </div>
        </div>
        
        <!-- 通關界面 -->
        <div id="levelCompleteScreen" class="fixed inset-0 z-20 bg-black/70 flex items-center justify-center p-6 hidden">
            <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 max-w-sm w-full animate-scale-in">
                <div id="celebrationContainer" class="relative h-40 -mt-20 mb-4">
                    <!-- 煙火和星星效果將在這裡動態生成 -->
                    <svg class="w-32 h-32 mx-auto trophy-glow" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 16.5L9 20L10 22H14L15 20L12 16.5Z" fill="#FFC107"/>
                        <path d="M12 15C8.13401 15 5 11.866 5 8V4H19V8C19 11.866 15.866 15 12 15Z" fill="#FFC107"/>
                        <path d="M5 2H19V4H5V2Z" fill="#FFC107"/>
                        <path d="M11 8.5C11 8.22386 11.2239 8 11.5 8H12.5C12.7761 8 13 8.22386 13 8.5V11.5C13 11.7761 12.7761 12 12.5 12H11.5C11.2239 12 11 11.7761 11 11.5V8.5Z" fill="#FFD54F"/>
                        <path d="M8 4H5C5 2.34315 6.34315 1 8 1V4Z" fill="#CFD8DC"/>
                        <path d="M16 4H19C19 2.34315 17.6569 1 16 1V4Z" fill="#CFD8DC"/>
                    </svg>
                </div>
                
                <h2 class="text-3xl font-bold text-primary mb-2 text-center">通關成功!</h2>
                <div class="text-center mb-6">
                    <p class="text-lg">你的分數: <span id="finalScore" class="font-bold">0</span></p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">完成時間: <span id="completionTime" class="font-bold">0</span> 秒</p>
                </div>
                
                <div class="space-y-3">
                    <button id="nextLevelButton" class="w-full bg-primary hover:bg-primary/90 text-white font-bold py-3 px-6 rounded-xl text-lg shadow-md transform transition hover:scale-105">
                        下一關卡
                    </button>
                    <button id="replayLevelButton" class="w-full bg-secondary hover:bg-secondary/90 text-white font-bold py-3 px-6 rounded-xl text-lg shadow-md transform transition hover:scale-105">
                        再次挑戰
                    </button>
                    <button id="returnToMapButton" class="w-full bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-xl text-lg shadow-md transform transition hover:scale-105">
                        返回地圖
                    </button>
                </div>
            </div>
        </div>
        
        <!-- 失敗界面 -->
        <div id="gameOverScreen" class="fixed inset-0 z-20 bg-black/70 flex items-center justify-center p-6 hidden">
            <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 max-w-sm w-full animate-scale-in">
                <h2 class="text-3xl font-bold text-danger mb-6 text-center">遊戲結束</h2>
                
                <div class="text-center mb-6">
                    <p class="text-lg">你的分數: <span id="gameOverScore" class="font-bold">0</span></p>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">目標分數: <span id="targetScore" class="font-bold">0</span></p>
                    <p class="text-md">再接再厲!</p>
                </div>
                
                <div class="space-y-3">
                    <button id="tryAgainButton" class="w-full bg-primary hover:bg-primary/90 text-white font-bold py-3 px-6 rounded-xl text-lg shadow-md transform transition hover:scale-105">
                        再試一次
                    </button>
                    <button id="returnToMenuButton" class="w-full bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-xl text-lg shadow-md transform transition hover:scale-105">
                        返回選單
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 確保在DOM加載完成後執行JavaScript代碼
        document.addEventListener('DOMContentLoaded', function() {
            console.log("DOM loaded, initializing game...");
            
            // 檢測暗色模式
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.documentElement.classList.add('dark');
            }
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
                if (event.matches) {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.remove('dark');
                }
            });
            
            // 常量和配置
            const COLORS = [
                '#4F46E5', // primary
                '#EC4899', // secondary
                '#10B981', // success
                '#F59E0B', // warning
                '#8B5CF6', // purple
                '#06B6D4'  // cyan
            ];
            
            // 關卡設定
            const LEVELS = [
                {
                    name: "新手村",
                    target: 100,
                    wordPool: ["你", "好", "我", "他", "她", "它", "是", "的", "了", "在", "有", "和", "不", "來", "去", "說", "看", "吃", "大", "小"],
                    dropSpeed: { min: 8, max: 12 },
                    spawnInterval: 3000,
                    backgroundColor: '#E0E7FF'
                },
                {
                    name: "進階森林",
                    target: 200,
                    wordPool: ["學校", "老師", "同學", "朋友", "媽媽", "爸爸", "喜歡", "快樂", "時間", "天氣", "早上", "中午", "晚上", "今天", "明天", "電腦", "手機", "水果", "運動", "遊戲"],
                    dropSpeed: { min: 5, max: 10 },
                    spawnInterval: 2500,
                    backgroundColor: '#ECFDF5'
                },
                {
                    name: "挑戰高原",
                    target: 300,
                    wordPool: ["電腦", "學習", "打字", "速度", "練習", "成功", "挑戰", "開心", "進步", "完成", "經驗", "時間", "空間", "宇宙", "恐龍", "科學", "藝術", "創造", "想像", "冒險"],
                    dropSpeed: { min: 4, max: 8 },
                    spawnInterval: 2000,
                    backgroundColor: '#FEF3C7'
                },
                {
                    name: "拼音海洋",
                    target: 400,
                    wordPool: ["ㄅㄆㄇㄈ", "ㄉㄊㄋㄌ", "ㄍㄎㄏ", "ㄐㄑㄒ", "ㄓㄔㄕㄖ", "ㄗㄘㄙ", "ㄧㄨㄩ", "ㄚㄛㄜㄝ", "ㄞㄟㄠㄡ", "ㄢㄣㄤㄥ", "ㄦ", "注音", "符號", "拼音", "聲調"],
                    dropSpeed: { min: 4, max: 7 },
                    spawnInterval: 1800,
                    backgroundColor: '#DBEAFE'
                },
                {
                    name: "太空站",
                    target: 500,
                    wordPool: ["cat", "dog", "run", "jump", "play", "book", "read", "write", "draw", "sing", "dance", "happy", "smile", "friend", "school", "teacher", "student", "hello", "goodbye", "thank"],
                    dropSpeed: { min: 3, max: 6 },
                    spawnInterval: 1500,
                    backgroundColor: '#EDE9FE'
                }
            ];
            
            // 遊戲狀態
            let gameState = {
                isPlaying: false,
                isPaused: false,
                currentLevel: 0,
                score: 0,
                words: [],
                gameTimer: null,
                spawnTimer: null,
                startTime: 0,
                progressLevel: [0, 0, 0, 0, 0], // 儲存每個關卡的進度百分比
                completedLevels: []  // 已完成的關卡
            };
            
            // DOM 元素
            const startScreen = document.getElementById('startScreen');
            const tutorialScreen = document.getElementById('tutorialScreen');
            const levelSelect = document.getElementById('levelSelect');
            const gameScreen = document.getElementById('gameScreen');
            const pauseScreen = document.getElementById('pauseScreen');
            const levelCompleteScreen = document.getElementById('levelCompleteScreen');
            const gameOverScreen = document.getElementById('gameOverScreen');
            
            const gameArea = document.getElementById('gameArea');
            const wordInput = document.getElementById('wordInput');
            const scoreDisplay = document.getElementById('scoreDisplay');
            const currentLevelDisplay = document.getElementById('currentLevel');
            const levelProgressBar = document.getElementById('levelProgressBar');
            const levelTarget = document.getElementById('levelTarget');
            const typingHint = document.getElementById('typingHint');
            
            const finalScore = document.getElementById('finalScore');
            const completionTime = document.getElementById('completionTime');
            const gameOverScore = document.getElementById('gameOverScore');
            const targetScore = document.getElementById('targetScore');
            const celebrationContainer = document.getElementById('celebrationContainer');
            
            // 按鈕事件處理
            const startBtn = document.getElementById('startBtn');
            const tutorialBtn = document.getElementById('tutorialBtn');
            const closeTutorialBtn = document.getElementById('closeTutorialBtn');
            const backFromLevelsBtn = document.getElementById('backFromLevelsBtn');
            
            // 確認按鈕是否存在,避免null錯誤
            console.log("Start button exists:", !!startBtn);
            console.log("Tutorial button exists:", !!tutorialBtn);
            
            // 按鈕事件處理 - 修復開始和教學按鈕
            if (startBtn) {
                startBtn.addEventListener('click', function() {
                    console.log("Start button clicked");
                    startScreen.classList.add('hidden');
                    levelSelect.classList.remove('hidden');
                    updateLevelButtons();
                });
            }
            
            if (tutorialBtn) {
                tutorialBtn.addEventListener('click', function() {
                    console.log("Tutorial button clicked");
                    startScreen.classList.add('hidden');
                    tutorialScreen.classList.remove('hidden');
                });
            }
            
            if (closeTutorialBtn) {
                closeTutorialBtn.addEventListener('click', function() {
                    tutorialScreen.classList.add('hidden');
                    startScreen.classList.remove('hidden');
                });
            }
            
            if (backFromLevelsBtn) {
                backFromLevelsBtn.addEventListener('click', function() {
                    levelSelect.classList.add('hidden');
                    startScreen.classList.remove('hidden');
                });
            }
            
            // 關卡選擇按鈕
            document.querySelectorAll('.level-button').forEach(button => {
                button.addEventListener('click', () => {
                    if (button.disabled) return;
                    
                    const level = parseInt(button.dataset.level) - 1; // 轉為0-索引
                    startGame(level);
                });
            });
            
            // 暫停按鈕
            document.getElementById('pauseButton').addEventListener('click', pauseGame);
            
            // 暫停選單按鈕
            document.getElementById('resumeButton').addEventListener('click', resumeGame);
            document.getElementById('restartLevelButton').addEventListener('click', () => {
                pauseScreen.classList.add('hidden');
                startGame(gameState.currentLevel);
            });
            document.getElementById('quitToMenuButton').addEventListener('click', () => {
                pauseScreen.classList.add('hidden');
                quitGame();
            });
            
            // 通關選單按鈕
            document.getElementById('nextLevelButton').addEventListener('click', () => {
                levelCompleteScreen.classList.add('hidden');
                startGame(gameState.currentLevel + 1);
            });
            document.getElementById('replayLevelButton').addEventListener('click', () => {
                levelCompleteScreen.classList.add('hidden');
                startGame(gameState.currentLevel);
            });
            document.getElementById('returnToMapButton').addEventListener('click', () => {
                levelCompleteScreen.classList.add('hidden');
                quitGame();
            });
            
            // 失敗選單按鈕
            document.getElementById('tryAgainButton').addEventListener('click', () => {
                gameOverScreen.classList.add('hidden');
                startGame(gameState.currentLevel);
            });
            document.getElementById('returnToMenuButton').addEventListener('click', () => {
                gameOverScreen.classList.add('hidden');
                quitGame();
            });
            
            // 更新關卡選擇按鈕
            function updateLevelButtons() {
                document.querySelectorAll('.level-button').forEach((button, index) => {
                    const level = index + 1;
                    const levelProgress = gameState.progressLevel[index];
                    const progressBar = button.querySelector('.level-progress');
                    
                    // 更新進度條
                    if (progressBar) {
                        progressBar.style.width = `${levelProgress}%`;
                    }
                    
                    // 解鎖關卡
                    if (level === 1 || gameState.completedLevels.includes(level - 1)) {
                        button.disabled = false;
                        button.classList.remove('opacity-60');
                        
                        // 更改已完成關卡的顏色
                        const levelNumber = button.querySelector('.level-number');
                        if (levelNumber) {
                            if (gameState.completedLevels.includes(level)) {
                                levelNumber.classList.remove('bg-gray-400');
                                levelNumber.classList.add('bg-success');
                            } else {
                                levelNumber.classList.remove('bg-gray-400');
                                levelNumber.classList.add('bg-primary');
                            }
                        }
                    }
                });
            }
            
            // 開始遊戲
            function startGame(level) {
                console.log(`Starting game at level ${level}`);
                
                // 確保關卡有效
                if (level < 0 || level >= LEVELS.length) {
                    level = 0;
                }
                
                // 重置遊戲狀態
                gameState.isPlaying = true;
                gameState.isPaused = false;
                gameState.currentLevel = level;
                gameState.score = 0;
                gameState.words = [];
                gameState.startTime = Date.now();
                
                // 更新界面
                levelSelect.classList.add('hidden');
                gameScreen.classList.remove('hidden');
                gameArea.innerHTML = '';
                scoreDisplay.textContent = '0';
                currentLevelDisplay.textContent = level + 1;
                levelProgressBar.style.width = '0%';
                
                // 設置關卡目標線
                const targetPercentage = (LEVELS[level].target / LEVELS[level].target) * 100;
                levelTarget.style.left = `${targetPercentage}%`;
                
                // 設置背景顏色
                gameArea.style.backgroundColor = LEVELS[level].backgroundColor;
                
                // 開始生成單詞
                gameState.spawnTimer = setInterval(() => {
                    if (!gameState.isPaused) {
                        spawnWord();
                    }
                }, LEVELS[level].spawnInterval);
                
                // 開始遊戲主循環
                gameState.gameTimer = setInterval(() => {
                    if (!gameState.isPaused) {
                        updateGame();
                    }
                }, 100); // 10 FPS
                
                // 聚焦輸入框
                wordInput.value = '';
                wordInput.focus();
                
                // 手機輸入優化
                wordInput.addEventListener('focus', () => {
                    // 一秒後滑動到底部,確保鍵盤顯示後也能看到輸入框
                    setTimeout(() => {
                        window.scrollTo(0, document.body.scrollHeight);
                    }, 1000);
                });
            }
            
            // 生成單詞
            function spawnWord() {
                const level = LEVELS[gameState.currentLevel];
                const word = level.wordPool[Math.floor(Math.random() * level.wordPool.length)];
                
                // 創建單詞元素
                const wordElement = document.createElement('div');
                wordElement.classList.add('word-drop', 'no-select');
                wordElement.innerText = word;
                
                // 隨機顏色
                const color = COLORS[Math.floor(Math.random() * COLORS.length)];
                wordElement.style.backgroundColor = `${color}20`; // 20% 透明度
                wordElement.style.color = color;
                wordElement.style.borderLeft = `4px solid ${color}`;
                
                // 計算位置
                const gameWidth = gameArea.offsetWidth;
                const wordWidth = word.length * 20 + 40; // 估計寬度
                const maxLeft = gameWidth - wordWidth - 20;
                const left = Math.max(20, Math.random() * maxLeft);
                
                wordElement.style.left = `${left}px`;
                
                // 設置動畫持續時間 (秒)
                const minSpeed = level.dropSpeed.min;
                const maxSpeed = level.dropSpeed.max;
                const dropSpeed = minSpeed + Math.random() * (maxSpeed - minSpeed);
                
                const gameHeight = gameArea.offsetHeight;
                wordElement.style.setProperty('--drop-distance', `${gameHeight}px`);
                wordElement.style.setProperty('--drop-time', `${dropSpeed}s`);
                
                // 添加到遊戲區域
                gameArea.appendChild(wordElement);
                
                // 添加到單詞列表
                gameState.words.push({
                    text: word,
                    element: wordElement,
                    timestamp: Date.now(),
                    speed: dropSpeed,
                    bottom: 0
                });
            }
            
            // 更新遊戲狀態
            function updateGame() {
                const gameHeight = gameArea.offsetHeight;
                
                // 更新每個單詞的位置
                gameState.words.forEach((word, index) => {
                    // 計算單詞當前位置
                    const elapsedTime = (Date.now() - word.timestamp) / 1000; // 經過的秒數
                    const progress = Math.min(1, elapsedTime / word.speed); // 進度百分比
                    const bottom = progress * gameHeight;
                    
                    word.bottom = bottom;
                    
                    // 檢查是否有單詞到達底部
                    if (bottom >= gameHeight && !word.element.classList.contains('word-remove')) {
                        gameOver();
                        return;
                    }
                });
                
                // 更新進度條
                const currentLevel = LEVELS[gameState.currentLevel];
                const progressPercentage = Math.min(100, (gameState.score / currentLevel.target) * 100);
                levelProgressBar.style.width = `${progressPercentage}%`;
                
                // 更新關卡進度
                gameState.progressLevel[gameState.currentLevel] = Math.max(
                    gameState.progressLevel[gameState.currentLevel], 
                    progressPercentage
                );
                
                // 檢查是否達到關卡目標
                if (gameState.score >= currentLevel.target && !gameState.isPaused) {
                    levelComplete();
                }
            }
            
            // 創建打字提示
            function updateTypingHint(currentInput) {
                // 清空提示
                typingHint.innerHTML = '';
                
                if (!currentInput) return;
                
                // 尋找匹配的單詞
                const matchingWords = gameState.words
                    .filter(word => word.text.startsWith(currentInput))
                    .sort((a, b) => a.bottom - b.bottom); // 按照從上到下的順序排序
                
                if (matchingWords.length > 0) {
                    const targetWord = matchingWords[0].text;
                    
                    // 顯示帶有匹配部分高亮的提示
                    for (let i = 0; i < targetWord.length; i++) {
                        const charSpan = document.createElement('span');
                        charSpan.classList.add('hint-char');
                        charSpan.innerText = targetWord[i];
                        
                        if (i < currentInput.length) {
                            // 已輸入的字符用綠色
                            charSpan.classList.add('text-success');
                        } else if (i === currentInput.length) {
                            // 當前需要輸入的字符特殊標記
                            charSpan.classList.add('text-primary', 'active');
                        }
                        
                        typingHint.appendChild(charSpan);
                    }
                    
                    // 高亮目標單詞
                    matchingWords[0].element.classList.add('ring-2', 'ring-primary', 'ring-offset-2');
                }
            }
            
            // 驗證輸入的單詞
            function checkWord(input) {
                if (!input) return;
                
                // 尋找匹配的單詞,優先消除在底部的單詞
                const index = gameState.words.findIndex(word => word.text === input);
                
                if (index !== -1) {
                    const matchedWord = gameState.words[index];
                    
                    // 標記為即將移除
                    matchedWord.element.classList.add('word-remove');
                    
                    // 增加分數 (基於單詞長度和剩餘時間)
                    const baseScore = matchedWord.text.length * 5;
                    const timeBonus = Math.floor((1 - matchedWord.bottom / gameArea.offsetHeight) * 10);
                    const points = baseScore + timeBonus;
                    
                    gameState.score += points;
                    scoreDisplay.textContent = gameState.score;
                    
                    // 顯示得分特效
                    showScoreEffect(matchedWord.element, points);
                    
                    // 創建消除特效
                    createRemoveEffect(matchedWord.element);
                    
                    // 從列表中移除
                    setTimeout(() => {
                        if (matchedWord.element.parentNode) {
                            matchedWord.element.remove();
                        }
                        
                        gameState.words = gameState.words.filter(w => w !== matchedWord);
                    }, 500);
                    
                    // 清空輸入
                    wordInput.value = '';
                    typingHint.innerHTML = '';
                    
                    return true;
                }
                
                return false;
            }
            
            // 顯示得分特效
            function showScoreEffect(element, points) {
                const rect = element.getBoundingClientRect();
                const scorePopup = document.createElement('div');
                
                scorePopup.className = 'absolute text-xl font-bold text-success pop-animation';
                scorePopup.innerText = `+${points}`;
                scorePopup.style.left = `${rect.left + rect.width / 2}px`;
                scorePopup.style.top = `${rect.top - 20}px`;
                scorePopup.style.transform = 'translate(-50%, -50%)';
                document.body.appendChild(scorePopup);
                
                // 向上飄動動畫
                let y = rect.top - 20;
                const interval = setInterval(() => {
                    y -= 2;
                    scorePopup.style.top = `${y}px`;
                    scorePopup.style.opacity = parseFloat(scorePopup.style.opacity || 1) - 0.05;
                    
                    if (parseFloat(scorePopup.style.opacity) <= 0) {
                        clearInterval(interval);
                        scorePopup.remove();
                    }
                }, 30);
            }
            
            // 創建消除特效
            function createRemoveEffect(element) {
                const rect = element.getBoundingClientRect();
                const centerX = rect.left + rect.width / 2;
                const centerY = rect.top + rect.height / 2;
                
                // 創建星星
                for (let i = 0; i < 6; i++) {
                    const star = document.createElement('div');
                    star.className = 'star';
                    
                    // 隨機位置偏移
                    const offsetX = (Math.random() - 0.5) * 40;
                    const offsetY = (Math.random() - 0.5) * 40;
                    
                    star.style.left = `${centerX + offsetX}px`;
                    star.style.top = `${centerY + offsetY}px`;
                    document.body.appendChild(star);
                    
                    // 1秒後移除星星
                    setTimeout(() => star.remove(), 1000);
                }
            }
            
            // 創建通關煙火特效
            function createCelebrationFireworks() {
                // 清空容器
                celebrationContainer.innerHTML = '';
                
                // 創建煙火
                for (let i = 0; i < 10; i++) {
                    setTimeout(() => {
                        const firework = document.createElement('div');
                        firework.className = 'firework';
                        
                        // 設置大小 (隨機)
                        const size = 30 + Math.random() * 50;
                        firework.style.width = `${size}px`;
                        firework.style.height = `${size}px`;
                        
                        // 隨機顏色
                        firework.style.backgroundColor = COLORS[Math.floor(Math.random() * COLORS.length)];
                        
                        // 隨機位置
                        firework.style.left = `${Math.random() * 100}%`;
                        firework.style.top = `${Math.random() * 100}%`;
                        
                        celebrationContainer.appendChild(firework);
                        
                        // 2秒後移除
                        setTimeout(() => firework.remove(), 2000);
                    }, i * 200);
                }
            }
            
            // 暫停遊戲
            function pauseGame() {
                if (!gameState.isPlaying || gameState.isPaused) return;
                
                gameState.isPaused = true;
                pauseScreen.classList.remove('hidden');
            }
            
            // 繼續遊戲
            function resumeGame() {
                if (!gameState.isPlaying || !gameState.isPaused) return;
                
                gameState.isPaused = false;
                pauseScreen.classList.add('hidden');
                wordInput.focus();
            }
            
            // 完成關卡
            function levelComplete() {
                // 暫停遊戲
                gameState.isPaused = true;
                clearInterval(gameState.gameTimer);
                clearInterval(gameState.spawnTimer);
                
                // 計算完成時間 (秒)
                const completionTimeValue = Math.floor((Date.now() - gameState.startTime) / 1000);
                
                // 更新完成關卡列表
                if (!gameState.completedLevels.includes(gameState.currentLevel + 1)) {
                    gameState.completedLevels.push(gameState.currentLevel + 1);
                }
                
                // 更新界面
                finalScore.textContent = gameState.score;
                completionTime.textContent = completionTimeValue;
                
                // 創建慶祝特效
                createCelebrationFireworks();
                
                // 顯示成功界面
                levelCompleteScreen.classList.remove('hidden');
                
                // 隱藏下一關按鈕如果是最後一關
                const nextLevelButton = document.getElementById('nextLevelButton');
                if (gameState.currentLevel >= LEVELS.length - 1) {
                    nextLevelButton.classList.add('hidden');
                } else {
                    nextLevelButton.classList.remove('hidden');
                }
            }
            
            // 遊戲結束
            function gameOver() {
                if (!gameState.isPlaying || gameState.isPaused) return;
                
                // 停止遊戲
                gameState.isPlaying = false;
                clearInterval(gameState.gameTimer);
                clearInterval(gameState.spawnTimer);
                
                // 更新界面
                gameOverScore.textContent = gameState.score;
                targetScore.textContent = LEVELS[gameState.currentLevel].target;
                
                // 顯示失敗界面
                gameOverScreen.classList.remove('hidden');
            }
            
            // 返回選單
            function quitGame() {
                // 停止遊戲
                gameState.isPlaying = false;
                gameState.isPaused = false;
                clearInterval(gameState.gameTimer);
                clearInterval(gameState.spawnTimer);
                
                // 隱藏遊戲界面
                gameScreen.classList.add('hidden');
                
                // 顯示關卡選擇
                levelSelect.classList.remove('hidden');
                
                // 更新關卡按鈕
                updateLevelButtons();
            }
            
            // 輸入事件處理
            wordInput.addEventListener('input', (e) => {
                const input = e.target.value.trim();
                
                // 更新提示
                updateTypingHint(input);
                
                // 檢查是否完成了一個單詞
                if (input && gameState.words.some(word => word.text === input)) {
                    checkWord(input);
                }
            });
            
            // 避免移動設備上的一些問題
            window.addEventListener('resize', () => {
                if (gameState.isPlaying) {
                    // 更新單詞的掉落距離
                    const gameHeight = gameArea.offsetHeight;
                    document.documentElement.style.setProperty('--game-height', `${gameHeight}px`);
                    
                    gameState.words.forEach(word => {
                        word.element.style.setProperty('--drop-distance', `${gameHeight}px`);
                    });
                }
            });
            
            // 在控制台輸出一些提示信息
            console.log("Game initialized");
        });
    </script>
</body>
</html>
"""

# 加載 HTML 內容到 WebView
webview.load_html(html_content)

# 顯示 WebView(全屏顯示)
webview.present('fullscreen')
