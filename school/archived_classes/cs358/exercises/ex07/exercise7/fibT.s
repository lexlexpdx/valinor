	.file	"fibT.c"
	.text
	.p2align 4
	.globl	fibT
	.type	fibT, @function
fibT:
.LFB39:
	.cfi_startproc
	endbr64
	movl	$1, %edx
	movl	$1, %eax
	movl	$1, %ecx
	cmpl	$2, %edi
	jg	.L2
	jmp	.L1
	.p2align 4,,10
	.p2align 3
.L10:
	movq	%rcx, %rax
.L2:
	subl	$1, %edi
	leaq	(%rax,%rdx), %rcx
	movq	%rax, %rdx
	cmpl	$2, %edi
	jne	.L10
.L1:
	movq	%rcx, %rax
	ret
	.cfi_endproc
.LFE39:
	.size	fibT, .-fibT
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"Usage : fibT n"
.LC1:
	.string	"fibT(%d) = %ld\n"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB41:
	.cfi_startproc
	endbr64
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	cmpl	$1, %edi
	jle	.L21
	movq	8(%rsi), %rdi
	movl	$10, %edx
	xorl	%esi, %esi
	call	strtol@PLT
	movl	$1, %esi
	movl	%eax, %edi
	cmpl	$2, %eax
	jle	.L14
	movl	$1, %ecx
	movl	$1, %edx
	jmp	.L13
	.p2align 4,,10
	.p2align 3
.L22:
	movq	%rsi, %rdx
.L13:
	subl	$1, %eax
	leaq	(%rdx,%rcx), %rsi
	movq	%rdx, %rcx
	cmpl	$2, %eax
	jne	.L22
.L14:
	movl	%edi, %edx
	movq	%rsi, %rcx
	movl	$2, %edi
	xorl	%eax, %eax
	leaq	.LC1(%rip), %rsi
	call	__printf_chk@PLT
	xorl	%eax, %eax
	popq	%rdx
	.cfi_remember_state
	.cfi_def_cfa_offset 8
	ret
.L21:
	.cfi_restore_state
	leaq	.LC0(%rip), %rdi
	call	puts@PLT
	xorl	%edi, %edi
	call	exit@PLT
	.cfi_endproc
.LFE41:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
