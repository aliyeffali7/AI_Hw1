# A* Search Algorithm – Report (Python version)

Bu layihə **A\*** axtarış alqoritmini üç fərqli rejimdə sınaqdan keçirir:
- UCS (Uniform Cost Search)
- A* (Euclidean heuristic)
- A* (Manhattan heuristic)

Kod: `astar.py`  
Daxil fayllar: `astar_small.txt`, `astar_medium.txt`

---

## 🔹 Test 1 — Small Graph (`astar_small.txt`)

### **1. Optimality**

**Sual:** Bütün üç rejim eyni xərci qaytarırmı?  
**Cavab:** ✅ Bəli, hamısı eyni nəticəni verir — **14**.  

Çünki hər iki heuristika həm **admissible**, həm də **consistent**dir.  
UCS həmişə optimal yolu tapır, buna görə A* nəticələri ilə eynidir.  

> Əgər nəticələr fərqli olsaydı, bu heuristikanın inadmissible olması demək olardı.

---

### **2. Efficiency**

**Sual:** Expanded və Runtime göstəriciləri arasında fərq necədir?  

| Mode | Expanded | Runtime (s) | İzah |
|-------|-----------|-------------|------|
| UCS | 5 | 0.000372 | Heuristika yoxdur, daha çox node genişləndirir |
| A* Euclidean | 4 | 0.000260 | Heuristika ilə daha az genişlənmə |
| A* Manhattan | 4 | 0.000032 | Ən sürətli nəticə |

**Gözlənilən qayda:**  
> UCS (h = 0) ≥ Euclidean ≥ Manhattan  
çünki Manhattan dəyərləri nöqtə-nöqtə Euclidean-dan böyükdür və daha aqressiv istiqamət göstərir.

---

### **3. Heuristic Validity**

**Sual:** Bütün kənarlar üçün bu şərtlər doğrudurmu?
- `w(u,v) ≥ Euclidean(u,v)`
- `w(u,v) ≥ Manhattan(u,v)`

**Cavab:** ✅ Bəli.  
Çıxışda “YES” nəticəsi göstərir ki, hər iki heuristika **admissible** və **consistent**dir.

---

## 🔹 Test 2 — Medium Graph (`astar_medium.txt`)

### **1. Optimality**

**Sual:** Bütün rejimlər eyni optimal xərc qaytarırmı?  
**Cavab:** ✅ Bəli, eyni nəticə — **10**.  
Heuristiklər yenə admissible və consistent olduğundan, hər üçü optimal yolu tapır.

---

### **2. Efficiency**

| Mode | Expanded | Runtime (s) | İzah |
|-------|-----------|-------------|------|
| UCS | 36 | 0.000462 | Heuristika yoxdur, çox node genişlənir |
| A* Euclidean | 36 | 0.000292 | Orta sürət |
| A* Manhattan | 36 | 0.000115 | Ən sürətli |

**Qeyd:** A* Manhattan, Euclidean-dan bir qədər daha aqressivdir və runtime baxımından daha yaxşı nəticə verir.

---

### **3. Heuristic Validity**

**Cavab:** ✅ Bəli, bütün kənar çəkiləri üçün həm Euclidean, həm də Manhattan şərtləri doğrudur.

---

## 📄 Nəticə

- Bütün rejimlər **optimal** nəticə verir.
- **Manhattan heuristikası** həm kiçik, həm də orta qrafda ən sürətli çıxış verir.
- Hər iki heuristika **admissible** və **consistent**dir.
- Nəticələr `astar.py` alqoritminin düzgün işlədiyini təsdiqləyir.

---

## 🧠 İstifadə Qaydası

Terminalda aşağıdakı əmri yaz:

```bash
python astar.py astar_small.txt
# və ya
python astar.py astar_medium.txt
