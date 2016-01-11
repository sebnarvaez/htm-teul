encodedWord = model.wordEncoder.encode('este')
spOutput = numpy.zeros(model.generalSP.getColumnDimensions(),
                    dtype=numpy.uint8)
model.generalSP.compute(encodedWord, True, spOutput)
tmInput = sorted(numpy.where(spOutput > 0)[0].flat)
module.compute(set(tmInput), True)
