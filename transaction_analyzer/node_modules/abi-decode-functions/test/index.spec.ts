/*tslint space-after-keywords: [2, "never"] */
declare function require(x: string): any

import { expect } from 'chai'
import AbiFunctions from '../src/index'

describe('index.js', () => {
  describe('isFunctionSelector', () => {
    let decoder: any
    beforeEach(() => {
      decoder = (new AbiFunctions('') as any)
    })
    it('true', async () => {
      const data = [
        { name: 'DUP1', pc: 54 },
        { name: 'PUSH4', pc: 55, pushData: '0x2c022289' },
        { name: 'EQ', pc: 60 },
        { name: 'PUSH2', pc: 61, pushData: '0x007d' },
        { name: 'JUMPI', pc: 64 }
      ]
      expect(decoder._isFunctionSelector(data)).to.be.true
    })
    it('false reason short', async () => {
      const data = [
        { name: 'DUP1', pc: 54 },
        { name: 'PUSH4', pc: 55, pushData: '0x2c022289' },
        { name: 'EQ', pc: 60 },
        { name: 'PUSH2', pc: 61, pushData: '0x007d' }
      ]
      expect(decoder._isFunctionSelector(data)).to.be.false
    })
    it('false reason invalid opcode', async () => {
      const data = [
        { name: 'DIV', pc: 54 },
        { name: 'PUSH4', pc: 55, pushData: '0x2c022289' },
        { name: 'EQ', pc: 60 },
        { name: 'PUSH2', pc: 61, pushData: '0x007d' },
        { name: 'JUMPI', pc: 64 }
      ]
      expect(decoder._isFunctionSelector(data)).to.be.false
    })
  })
  describe('parseCode', () => {
    const footerMetadata = '00a165627a7a723058208e0087b75d0ea5908b0776e3657eca75d4d0052a722dd2d3c6a4ad6236b359e90029'
    const opcodes = '0x608060405260043610610078576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680632c0222891461007d57'
    let decoder: any
    beforeEach(() => {
      decoder = (new AbiFunctions('') as any)
    })
    it('success', async () => {
      const result = decoder._parseCode(opcodes + footerMetadata)
      expect(result).to.be.a('array')
      expect(result).to.have.length(1)
    })
    it('return empty result when invalid args', async () => {
      const result = decoder._parseCode('hogehoge')
      expect(result).to.have.length(0)
    })
    it('return empty result when not contains function selector', async () => {
      const result = decoder._parseCode('0x1234567890abcdef' + footerMetadata)
      expect(result).to.have.length(0)
    })
  })
  describe('getFunctionIds', () => {
    const footerMetadata = '00a165627a7a723058208e0087b75d0ea5908b0776e3657eca75d4d0052a722dd2d3c6a4ad6236b359e90029'
    const opcodes = '0x608060405260043610610078576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680632c0222891461007d57'

    it('success', async () => {
      const decoder = new AbiFunctions(opcodes + footerMetadata)
      const result = decoder.getFunctionIds()
      expect(result).to.be.a('array')
      expect(result).to.have.length(1)
      expect(result[0]).to.equal('0x2c022289')
    })
    it('return empty result when invalid args', async () => {
      const decoder = new AbiFunctions('hogehoge')
      const result = decoder.getFunctionIds()
      expect(result).to.have.length(0)
    })
    it('return empty result when not contains function selector', async () => {
      const decoder = new AbiFunctions('0x1234567890abcdef' + footerMetadata)
      const result = decoder.getFunctionIds()
      expect(result).to.have.length(0)
    })
  })
  describe('find pc by function id', () => {
    const footerMetadata = '00a165627a7a723058208e0087b75d0ea5908b0776e3657eca75d4d0052a722dd2d3c6a4ad6236b359e90029'
    const opcodes = '0x608060405260043610610078576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680632c0222891461007d57'

    it('success', async () => {
      const decoder = new AbiFunctions(opcodes + footerMetadata)
      const result = decoder.findProgramCounter('0x2c022289')
      expect(result).to.be.a('number')
      expect(result).to.equal(125)
    })
    it('fail return undef. non exist id', async () => {
      const decoder = new AbiFunctions(opcodes + footerMetadata)
      const result = decoder.findProgramCounter('0x22222222')
      expect(result).to.be.null
    })
    it('fail return undef. when empty', async () => {
      const decoder = new AbiFunctions('hogehoge')
      const result = decoder.findProgramCounter('0x2c022289')
      expect(result).to.be.null
    })
    it('fail return undef. when opcodes is null', async () => {
      const decoder = new AbiFunctions(null)
      const result = decoder.findProgramCounter('0x2c022289')
      expect(result).to.be.null
    })
  })
})
