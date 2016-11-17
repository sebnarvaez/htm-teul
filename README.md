**BEWARE:** This Readme is under construction and porbably incomplete.

# Description
HTM-TEUL is an experiment to evaluate the use of the HTM theory on Natural 
Language Processing. TEUL stands for Task Execution Using Language. The
software allows you to give sentences in spanish or english in order to
execute a task in a virtual, controlled environment. You can find the data
used to train the learning system in Learning/Data.

I presented this project as my undergraduate "thesis". You may find the full text (in spanish) in my [ResearchGate](https://www.researchgate.net/publication/305114878_Desarrollo_de_un_modelo_HTM_para_la_ejecucion_de_tareas_utilizando_el_lenguaje_natural?ev=prf_pub).

# Requirements
* [Nupic](https://github.com/numenta/nupic) (Tested with v. 0.3.6 and v. 0.5.0)
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)
* [PyramsFinder](https://github.com/larvasapiens/PyramsFinder) (Included in Utils/)

# The Encoders

The following are use examples of the different encoders used in HTM-TEUL

## Custom Category Encoder:

A custom version of the Nupic's Category Encoder. Allows to reserve slots for additional categories at creation time.

```python
encoder = CustomCategoryEncoder(w=3, categoryList=["a", "b"], nAdditionalCategorySlots=1, forced=True)

encoder.encode("a")
#Out (Input in categoryList, previously assigned bits): 
array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], dtype=uint8)

encoder.encode("z")
#Out (Assigns the reserved slot):
array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], dtype=uint8)

encoder.encode("c")
#Out (No slots left, assigns <<Unknown>> classification):
array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=uint8)
```

## Randomized Letter Encoder:

A bit is assigned to each letter of the word (using a Category Encoder), and then a random string of bits is concatenated.

```python
encoder = RandomizedLetterEncoder(width=60, nRandBits=2, actBitsPerLetter=1)

encoder.encode('le')
# Out (Active bits: 12 ('l'), 32 ('e'), 54 and 57 (random)): 
array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0], dtype=uint8)

encoder.encode('la')
# Out (Active bits: 12 ('l'), 28 ('a'), 55 and 58 (random)): 
array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], dtype=uint8)
```

## Totally Random Encoder:

A random sequence of bits is assigned to each word.

```python
encoder = TotallyRandomEncoder(width=15, nActiveBits=3)

encoder.encode("a")
#Out (assigned bits): 
array([0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0], dtype=uint8)

encoder.encode("r")
#Out (assigned bits): 
array([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], dtype=uint8)
```

# Contact
If you have any questions, recommendations, need support, or if you just liked the project, 
I'll be happy to read your emails at sebasnr95@gmail.com

