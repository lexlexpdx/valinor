	.file	"fib.c"
	.text
	.p2align 4
	.globl	fib
	.type	fib, @function
fib:
.LFB39:
	.cfi_startproc
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	movl	$1, %r15d
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$136, %rsp
	.cfi_def_cfa_offset 192
	cmpl	$2, %edi
	jle	.L1
	leal	-2(%rdi), %eax
	movl	%edi, %ebp
	xorl	%r15d, %r15d
	andl	$-2, %eax
	movl	%ebp, %ebx
	subl	%eax, %edi
	movl	%edi, 88(%rsp)
.L5:
	movl	88(%rsp), %eax
	leal	-1(%rbx), %r13d
	cmpl	%eax, %ebx
	je	.L50
.L3:
	leal	-3(%rbx), %eax
	movl	%r13d, %edi
	movq	%r15, 48(%rsp)
	xorl	%r14d, %r14d
	andl	$-2, %eax
	movl	%ebx, %r15d
	movl	%r13d, %ebx
	subl	%eax, %edi
	movl	%edi, 76(%rsp)
.L8:
	leal	-1(%rbx), %ebp
	cmpl	%ebx, 76(%rsp)
	je	.L51
.L6:
	leal	-3(%rbx), %edx
	movl	%ebp, %eax
	movl	%ebx, 60(%rsp)
	xorl	%r12d, %r12d
	andl	$-2, %edx
	subl	%edx, %eax
	movl	%eax, 80(%rsp)
.L11:
	leal	-1(%rbp), %ebx
	cmpl	%ebp, 80(%rsp)
	je	.L52
	leal	-3(%rbp), %edx
	movl	%ebx, %eax
	movq	%r14, 64(%rsp)
	xorl	%r13d, %r13d
	andl	$-2, %edx
	subl	%edx, %eax
	movl	%eax, 84(%rsp)
	movq	%r12, %rax
	movq	%r13, %r12
.L14:
	leal	-1(%rbx), %r13d
	cmpl	%ebx, 84(%rsp)
	je	.L53
	leal	-3(%rbx), %r8d
	movl	%r13d, %edx
	movl	%r15d, 72(%rsp)
	xorl	%r14d, %r14d
	andl	$-2, %r8d
	movq	%rax, %r11
	movl	%ebx, %esi
	movq	%r12, %rcx
	subl	%r8d, %edx
	movl	%ebp, %r8d
	movl	%edx, %r15d
.L17:
	cmpl	%r15d, %r13d
	je	.L54
	leal	-4(%r13), %ebx
	leal	-3(%r13), %eax
	xorl	%ebp, %ebp
	andl	$-2, %eax
	movl	%ebx, %r10d
	leal	-6(%r13), %edi
	subl	%eax, %r10d
	movl	%ebx, %eax
	andl	$-2, %eax
	movl	%r10d, 16(%rsp)
	movl	%r8d, %r10d
	leal	2(%rbx), %r8d
	subl	%eax, %edi
	cmpl	%ebx, 16(%rsp)
	je	.L55
.L18:
	leal	-2(%rbx), %eax
	movl	%ebx, %r9d
	movl	%r8d, %edx
	xorl	%r12d, %r12d
	andl	$-2, %r9d
	movl	%eax, 12(%rsp)
	subl	%r9d, %edx
	movl	%eax, %r9d
	movl	%edx, 44(%rsp)
	movl	%edi, %edx
	movl	%ebx, %edi
.L23:
	movl	44(%rsp), %eax
	cmpl	%eax, %r8d
	je	.L56
	movl	12(%rsp), %eax
	leal	-4(%r8), %ebx
	movq	%rcx, 32(%rsp)
	movl	%r10d, 20(%rsp)
	movl	%edi, %r10d
	andl	$-2, %eax
	movq	%r11, 24(%rsp)
	movl	%r15d, %r11d
	movq	%r12, %r15
	subl	%eax, %ebx
	xorl	%eax, %eax
	movl	%edx, 40(%rsp)
	movq	%rbp, %r12
	movl	%ebx, 56(%rsp)
	movq	%rax, %rdx
	movl	%edi, %ebx
.L26:
	movl	%ebx, %ebp
	cmpl	$2, %ebx
	je	.L57
	xorl	%ecx, %ecx
.L24:
	leal	-1(%rbp), %edi
	movl	%r9d, 124(%rsp)
	subl	$2, %ebp
	movl	%r11d, 120(%rsp)
	movl	%r10d, 116(%rsp)
	movq	%rcx, 104(%rsp)
	movq	%rdx, 96(%rsp)
	movl	%r8d, 112(%rsp)
	movl	%esi, 92(%rsp)
	call	fib
	movq	104(%rsp), %rcx
	movl	92(%rsp), %esi
	movl	112(%rsp), %r8d
	movq	96(%rsp), %rdx
	addq	%rax, %rcx
	cmpl	$2, %ebp
	movl	116(%rsp), %r10d
	movl	120(%rsp), %r11d
	movl	124(%rsp), %r9d
	jg	.L24
	leaq	1(%rdx,%rcx), %rdx
	subl	$2, %ebx
	cmpl	%ebx, 56(%rsp)
	jne	.L26
	movq	%r12, %rbp
	movq	%rdx, %rax
	movq	%r15, %r12
	movl	%r10d, %edi
	movl	%r11d, %r15d
	movq	32(%rsp), %rcx
	movl	20(%rsp), %r10d
	movq	24(%rsp), %r11
	movl	40(%rsp), %edx
.L25:
	subl	$2, %r8d
	subl	$2, 12(%rsp)
	leaq	1(%r12,%rax), %r12
	subl	$2, %edi
	cmpl	$2, %r8d
	jne	.L23
	movl	%edx, %edi
	movl	%r9d, %eax
	leaq	1(%rbp,%r12), %rbp
	cmpl	%eax, %edi
	je	.L45
.L58:
	movl	%eax, %ebx
	leal	2(%rbx), %r8d
	cmpl	%ebx, 16(%rsp)
	jne	.L18
.L55:
	movl	%r10d, %r8d
	addq	$1, %rbp
.L19:
	subl	$2, %r13d
	leaq	1(%r14,%rbp), %r14
	cmpl	$2, %r13d
	jne	.L17
	movl	72(%rsp), %r15d
	movl	%r8d, %ebp
	movq	%r11, %rax
	movl	%esi, %ebx
	movq	%rcx, %r12
.L16:
	subl	$2, %ebx
	leaq	1(%r12,%r14), %r12
	cmpl	$2, %ebx
	jne	.L14
	movq	64(%rsp), %r14
	movq	%r12, %r13
	movq	%rax, %r12
.L13:
	subl	$2, %ebp
	leaq	1(%r12,%r13), %r12
	cmpl	$2, %ebp
	jne	.L11
	movl	60(%rsp), %ebx
	leaq	1(%r14,%r12), %r14
	subl	$2, %ebx
	cmpl	$2, %ebx
	jne	.L8
.L59:
	movl	%r15d, %ebx
	movq	48(%rsp), %r15
	subl	$2, %ebx
	leaq	1(%r15,%r14), %r15
	cmpl	$2, %ebx
	jne	.L5
.L60:
	addq	$1, %r15
	jmp	.L1
	.p2align 4,,10
	.p2align 3
.L56:
	addq	$1, %r12
	movl	%edx, %edi
	movl	%r9d, %eax
	leaq	1(%rbp,%r12), %rbp
	cmpl	%eax, %edi
	jne	.L58
.L45:
	movl	%r10d, %r8d
	jmp	.L19
	.p2align 4,,10
	.p2align 3
.L57:
	movq	%rdx, %rax
	movq	%r12, %rbp
	movl	%r10d, %edi
	movq	%r15, %r12
	movq	32(%rsp), %rcx
	movl	%r11d, %r15d
	movl	40(%rsp), %edx
	addq	$1, %rax
	movl	20(%rsp), %r10d
	movq	24(%rsp), %r11
	jmp	.L25
.L54:
	movl	72(%rsp), %r15d
	movl	%r8d, %ebp
	movq	%r11, %rax
	movl	%esi, %ebx
	movq	%rcx, %r12
	addq	$1, %r14
	jmp	.L16
.L53:
	movq	%r12, %r13
	movq	64(%rsp), %r14
	movq	%rax, %r12
	addq	$1, %r13
	jmp	.L13
.L52:
	movl	60(%rsp), %ebx
	addq	$1, %r12
	leaq	1(%r14,%r12), %r14
	subl	$2, %ebx
	cmpl	$2, %ebx
	je	.L59
	leal	-1(%rbx), %ebp
	cmpl	%ebx, 76(%rsp)
	jne	.L6
.L51:
	movl	%r15d, %ebx
	movq	48(%rsp), %r15
	addq	$1, %r14
	subl	$2, %ebx
	leaq	1(%r15,%r14), %r15
	cmpl	$2, %ebx
	je	.L60
	movl	88(%rsp), %eax
	leal	-1(%rbx), %r13d
	cmpl	%eax, %ebx
	jne	.L3
.L50:
	addq	$2, %r15
.L1:
	addq	$136, %rsp
	.cfi_def_cfa_offset 56
	movq	%r15, %rax
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE39:
	.size	fib, .-fib
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"Usage : fib n"
.LC1:
	.string	"fib(%d) = %ld\n"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB40:
	.cfi_startproc
	endbr64
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	cmpl	$1, %edi
	jle	.L64
	movq	8(%rsi), %rdi
	movl	$10, %edx
	xorl	%esi, %esi
	call	strtol@PLT
	movl	%eax, %edi
	movl	%eax, %ebx
	call	fib
	movl	%ebx, %edx
	movl	$2, %edi
	leaq	.LC1(%rip), %rsi
	movq	%rax, %rcx
	xorl	%eax, %eax
	call	__printf_chk@PLT
	xorl	%eax, %eax
	popq	%rbx
	.cfi_remember_state
	.cfi_def_cfa_offset 8
	ret
.L64:
	.cfi_restore_state
	leaq	.LC0(%rip), %rdi
	call	puts@PLT
	xorl	%edi, %edi
	call	exit@PLT
	.cfi_endproc
.LFE40:
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
