import { describe, it, expect } from 'vitest';
import { normalizeVi, readNumber, splitSpeech } from './vi-normalize';

describe('readNumber', () => {
  it.each([
    ['0', 'không'], ['5', 'năm'], ['10', 'mười'], ['15', 'mười lăm'], ['21', 'hai mươi mốt'], ['24', 'hai mươi tư'],
    ['105', 'một trăm lẻ năm'], ['48', 'bốn mươi tám'], ['2005', 'hai nghìn không trăm lẻ năm'],
    ['1984', 'một nghìn chín trăm tám mươi tư'], ['30000', 'ba mươi nghìn'], ['1200000', 'một triệu hai trăm nghìn'],
    ['1000005', 'một triệu không trăm lẻ năm'],
  ])('%s → %s', (n, w) => expect(readNumber(n)).toBe(w));
});

describe('normalizeVi', () => {
  const n = normalizeVi;
  it('dates and times', () => {
    expect(n('14h00 ngày 19/08/2005')).toBe('mười bốn giờ ngày mười chín tháng tám năm hai nghìn không trăm lẻ năm');
    expect(n('khoảng từ 11h45 đến 13h00')).toBe('khoảng từ mười một giờ bốn mươi lăm phút đến mười ba giờ');
    expect(n('ngày 5/4')).toBe('ngày mùng năm tháng tư');
    expect(n('lúc 20:30')).toBe('lúc hai mươi giờ ba mươi phút');
  });
  it('money, units, dimensions', () => {
    expect(n('không dưới 30.000 USD')).toBe('không dưới ba mươi nghìn đô la Mỹ');
    expect(n('kích thước 40cm x 120cm')).toBe('kích thước bốn mươi xăng-ti-mét nhân một trăm hai mươi xăng-ti-mét');
    expect(n('cách cửa sau 80m')).toBe('cách cửa sau tám mươi mét');
    expect(n('giá 500.000đ')).toBe('giá năm trăm nghìn đồng');
    expect(n('nặng 3,5kg')).toBe('nặng ba phẩy năm ki-lô-gam');
  });
  it('abbreviations, acronyms, headings, roman numerals', () => {
    expect(n('Ống nhựa PVC')).toBe('Ống nhựa pê vê xê');
    expect(n('**BIÊN BẢN KHÁM NGHIỆM HIỆN TRƯỜNG**')).toBe('biên bản khám nghiệm hiện trường');
    expect(n('UBND TP. Hội An')).toBe('Ủy ban nhân dân thành phố Hội An');
    expect(n('đầu thế kỷ XIX')).toBe('đầu thế kỷ mười chín');
    expect(n('số 48 đường Trần Phú (phường Minh An).')).toBe('số bốn mươi tám đường Trần Phú, phường Minh An.');
    expect(n('SĐT: 0905123456')).toBe('số điện thoại: không chín không năm một hai ba bốn năm sáu');
  });
  it('keeps plain Vietnamese untouched', () => {
    const s = 'Cửa nách phía sau khép hờ, ổ khóa không có dấu hiệu cạy phá.';
    expect(n(s)).toBe(s);
  });
});

describe('splitSpeech', () => {
  it('never cuts mid-sentence when sentences fit, pauses longer at paragraph ends', () => {
    const text = 'Câu một ngắn. Câu hai cũng ngắn.\nĐoạn mới bắt đầu ở đây.';
    const segs = splitSpeech(text, 180);
    expect(segs.map((s) => s.text)).toEqual(['Câu một ngắn. Câu hai cũng ngắn.', 'Đoạn mới bắt đầu ở đây.']);
    expect(segs[0].pause).toBeGreaterThan(0.3);
  });
  it('splits a long sentence at commas, within the limit', () => {
    const long = Array.from({ length: 12 }, (_, i) => `vế câu thứ ${i} khá dài một chút`).join(', ') + '.';
    const segs = splitSpeech(long, 120);
    expect(segs.length).toBeGreaterThan(2);
    segs.forEach((s) => expect(s.text.length).toBeLessThanOrEqual(121));
  });
  it('headings get a period and a longer pause', () => {
    const [h] = splitSpeech('biên bản khám nghiệm\nNội dung.');
    expect(h.text).toBe('biên bản khám nghiệm.');
    expect(h.pause).toBeGreaterThan(0.5);
  });
});

describe('codes and technical text', () => {
  const n = normalizeVi;
  it.each([
    ['đoàn tàu SE3', 'đoàn tàu ét e ba'],
    ['súng K54', 'súng ca năm mươi tư'],
    ['tàu cá QN-9288-TS', 'tàu cá quy nờ chín hai tám tám tê ét'],
    ['máy chính 50kVA', 'máy chính năm mươi ki-lô vôn ampe'],
    ['bình ắc-quy 24V', 'bình ắc-quy hai mươi tư vôn'],
    ['vàng 24K', 'vàng hai mươi tư ca-ra'],
    ['Mực nước +0.45m', 'Mực nước cộng không phẩy bốn lăm mét'],
    ['cao khoảng 1m75', 'cao khoảng một mét bảy mươi lăm'],
    ['xem ảnh d07', 'xem ảnh tài liệu số bảy'],
    ['phòng 204 nhà A6', 'phòng hai trăm lẻ bốn nhà a sáu'],
  ])('%s', (a, b) => expect(n(a)).toBe(b));
});
