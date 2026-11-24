import json, glob, os, re

for bible_path in sorted(glob.glob('authoring/*/bible.md')):
    case_id = bible_path.split('/')[1]
    case_json_path = f'public/cases/{case_id}/case.json'
    if not os.path.exists(case_json_path):
        continue
    with open(case_json_path, 'r', encoding='utf-8') as f:
        case = json.load(f)
    with open(bible_path, 'r', encoding='utf-8') as f:
        bible_content = f.read()
    
    stages = case.get('stages', [])
    questions = case.get('questions', [])
    
    sec4_lines = ['## 4. Cấu trúc câu hỏi & Trọng điểm (Đã nâng cấp độ khó x5)']
    for s_idx, st in enumerate(stages):
        sec4_lines.append(f'- **Trọng điểm {s_idx + 1}**: {st.get("title", "")}')
        docs = st.get('documents', [])
        if docs:
            sec4_lines.append(f'  - Tài liệu: {docs[0]} – {docs[-1]} ({len(docs)} tài liệu)')
        st_qs = [q for q in questions if q.get('stage_index') == s_idx]
        for q in st_qs:
            q_id = q.get('id')
            q_type = q.get('type')
            prompt = q.get('prompt', '')
            ans = q.get('answer')
            if q_type == 'evidence':
                need = q.get('need', len(ans) if isinstance(ans, list) else 1)
                sec4_lines.append(f'  - **Câu hỏi {q_id}** (`evidence` - `need: {need}`): {prompt} Đáp án: `{ans}`.')
            elif q_type == 'line':
                sec4_lines.append(f'  - **Câu hỏi {q_id}** (`line`): {prompt} Đáp án: `{ans}`.')
            elif q_type == 'choice':
                opts = q.get('options', [])
                ans_idx = ans[0] if isinstance(ans, list) and len(ans) > 0 else 0
                ans_text = opts[ans_idx] if ans_idx < len(opts) else str(ans)
                if len(ans_text) > 100:
                    ans_text = ans_text[:97] + '...'
                sec4_lines.append(f'  - **Câu hỏi {q_id}** (`choice`): {prompt} Đáp án: Lựa chọn {ans_idx + 1} ("{ans_text}").')
    
    new_sec4 = '\n'.join(sec4_lines) + '\n'
    
    # Check what heading is used in bible_content for section 4 or questions
    sec4_match = re.search(r'(## (?:4\.\s*)?Cấu trúc câu hỏi.*|## (?:4\.\s*)?Hệ thống câu hỏi.*|## (?:4\.\s*)?Trọng điểm.*)', bible_content, re.IGNORECASE)
    if sec4_match:
        updated_content = bible_content[:sec4_match.start()] + new_sec4
        with open(bible_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f'Synced {case_id}')
    else:
        # Check if there is another heading or append at the end
        print(f'Check headings for {case_id}')
