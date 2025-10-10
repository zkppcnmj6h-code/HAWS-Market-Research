---

## Quick commit steps (copy/paste)

```bash
# 1) Ensure branch
git switch -c sprint-3-docs 2>/dev/null || git switch sprint-3-docs

# 2) Create folders and file
mkdir -p "HAWS_99_COORDINATOR_TOOLS/04_Templates"
nano "HAWS_99_COORDINATOR_TOOLS/04_Templates/PR_Template.md"
# paste FULL template, save (Ctrl+O, Enter), exit (Ctrl+X)

# 3) Verify + commit
./bin/haws-verify
git add "HAWS_99_COORDINATOR_TOOLS/04_Templates/PR_Template.md"
git commit -m "docs: add standardized Pull Request description template (v1.0)"
git push -u origin sprint-3-docs---
document_type: template
workstream: HAWS_99_COORDINATOR_TOOLS
template_type: Pull_Request_Description
status: Active
created: 2025-10-09
maintained_by: Strategic Coordinator
reviewed_by: Strategic Advisor
---

# HAWS Pull Request Description Template

**Title:**  
`<short summary of the change>`

---

### **1. Summary**
Provide a concise summary of what this Pull Request introduces or modifies.  
Explain *what* has changed and *why* — connecting tactical work to strategic intent or sprint goals.

---

### **2. Artifacts Added / Modified**

| File Path | Description |
|------------|--------------|
| `<path/to/file>` | Purpose or notes |

---

### **3. Rationale**
Explain how this change supports the current sprint, milestone, or directive.

---

### **4. Change Type**
- [ ] 📄 Documentation  
- [ ] 🧩 Feature Code  
- [ ] ⚙️ Configuration / Script  
- [ ] 🧪 Test or Validation  
- [ ] 🔒 Security / Access Control  

---

### **5. Verification Checklist**
- [ ] `./bin/haws-verify` passes  
- [ ] Files have correct metadata headers  
- [ ] Markdown renders correctly on GitHub  
- [ ] No backup or lock files  
- [ ] Change log updated  

Optional tagging:
```bash
git tag -a <version> -m "Brief description"
git push origin <version>
