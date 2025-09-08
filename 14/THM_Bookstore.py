"""
On reprend doucement avec un code simple/trivial. Nous sommes sur le CTF Bookstore. Après un API Rest Fuzz (nous avons utilisé wfuzz, donc 
potentiel de script pour demain), nous parvenons à récupérer un PIN nous permettant de nous connecter (revshell). Nous avons dans le folder user 
un binaire, que nous avons analysé avec Ghidra : 
void main(void)

{
  long in_FS_OFFSET;
  uint local_1c;
  uint local_18;
  uint local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setuid(0);
  local_18 = 0x5db3;
  puts("What\'s The Magic Number?!");
  __isoc99_scanf(&DAT_001008ee,&local_1c);
  local_14 = local_1c ^ 0x1116 ^ local_18;
  if (local_14 == 0x5dcd21f4) {
    system("/bin/bash -p");
  }
  else {
    puts("Incorrect Try Harder");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}


"""

local_1c = 0x5dcd21f4 ^ 0x1116 ^ 0x5db3
print(local_1c)